import torch
import pandas


class CartTree:
    def __init__(self, max_depth=3):
        self.__tree = None
        self.__max_depth = max_depth

    def clear(self):
        self.__tree = None

    def get_model(self):
        return self.__tree

    def train(self, X, y):
        self.__tree = self.create_tree(X, y, self.__max_depth)
        print("done training")

    def create_tree(self, X, y, depth=1):
        print(depth)
        # 叶子节点的标签值是tensor(3)
        if depth == 0:  # if can't continue constructing tree deeper
            return self.count_majority(y)

        if torch.eq(y, y[0].item()).sum() == y.size()[0]:
            # if current samples all belong to the same class
            return y[0]

        if len(X) == 1:  # if only one sample left
            return self.count_majority(y)

        best_feature, best_threshold = self.choose_best_feature_to_split(X, y)
        # name current node as ...
        current_node = str(best_feature) + ":" + str(best_threshold.item())
        if best_feature == -1:  # if no best feature
            return self.count_majority(y)

        myTree = {current_node: {}}

        # (recurrence) construct
        X_left, y_right = self.split_node(X, y, best_feature, best_threshold, 'left')
        myTree[current_node]['<=' + str(round(float(best_threshold), 3))] = \
            self.create_tree(X_left, y_right, depth - 1)
        X_right, y_right = self.split_node(X, y, best_feature, best_threshold, 'right')
        myTree[current_node]['>' + str(round(float(best_threshold), 3))] = \
            self.create_tree(X_right, y_right, depth - 1)
        return myTree

    def choose_best_feature_to_split(self, X, y):
        n_samples = len(X)
        n_features = len(X[0])
        bestGiniGain = 1.0
        bestFeature = -1
        best_value = ""
        for dimension_i in range(n_features):  # 遍历特征
            featList = X[:, dimension_i]
            featList = torch.unique(featList)  # unique and sorted
            for feature_value in featList:  # 遍历所有的特征值
                GiniGain = 0.0
                # binary split
                left_sub_X, left_sub_y = \
                    self.split_node(X, y, dimension_i, feature_value, 'left')
                right_sub_X, right_sub_y = \
                    self.split_node(X, y, dimension_i, feature_value, 'right')
                left_proportion = len(left_sub_X) / float(n_samples)
                right_proportion = len(right_sub_X) / float(n_samples)

                GiniGain += left_proportion * self.cal_gini(left_sub_X, left_sub_y)
                GiniGain += right_proportion * self.cal_gini(right_sub_X, right_sub_y)

                # print GiniGain
                if GiniGain < bestGiniGain:  # get the best gini gain
                    bestGiniGain = GiniGain
                    bestFeature = dimension_i
                    best_value = feature_value
        return bestFeature, best_value

    def cal_gini(self, X, y):  # 计算一个数据集的gini系数
        n_samples = len(X)
        labelCounts = {}
        for sample_i in range(n_samples):
            if y[sample_i].item() not in labelCounts.keys():
                labelCounts[y[sample_i].item()] = 0
            labelCounts[y[sample_i].item()] += 1
        gini = 1
        for label in labelCounts.keys():
            prop = float(labelCounts[label]) / n_samples
            gini -= prop * prop
        return gini

    def split_node(self, X, y, axis, value, direction):  # 根据特征、特征值和方向划分数据集
        child_X = torch.empty(0, X.size()[1], dtype=torch.float64)  # empty
        child_y = torch.empty(0, dtype=torch.long)
        # child_y = []
        if direction == 'left':
            for sample_i in range(len(X)):
                if X[sample_i][axis] <= value:
                    child_X = torch.cat((
                        child_X, X[sample_i].unsqueeze(0)), dim=0)
                    child_y = torch.cat((
                        child_y, y[sample_i].unsqueeze(0)))
                    # child_y.append(y[sample_i])
        else:
            for sample_i in range(len(X)):
                if X[sample_i][axis] > value:
                    child_X = torch.cat((
                        child_X, X[sample_i].unsqueeze(0)), dim=0)
                    child_y = torch.cat((
                        child_y, y[sample_i].unsqueeze(0)))

        return child_X, child_y

    def count_majority(self, y):  # 多数表决
        # 输入是tensor,返回时tensor
        return y.mode()[0]

    def validate(self, X, y):
        error_list = torch.ones_like(y, dtype=torch.long)  # 返回预测对或者错，而不是返回预测的结果(对为0，错为1，方便计算预测错误的个数)
        predict_result = torch.ones_like(y, dtype=torch.long)
        for i in range(len(X)):
            res = self.predict(X[i])
            # print(res)
            error_list[i] = res != y[i]
            predict_result[i] = res
            # print predict(tree,dataMatrix[i]),classList[i]
        return error_list, predict_result

    def predict(self, sample):
        if self.__tree is None:
            print("tree not trained yet!")
            return
        return self.__predict(sample, self.__tree)

    def __predict(self, sample, tree):
        # 返回的是叶子节点是tensor
        # sample like: tensor([2, 3, 4, 5, 6])
        if type(tree) is not dict:
            return tree
        root = list(tree.keys())[0]
        feature, threshold = root.split(":")  # 取出根节点，得到最优特征和阀值
        feature = int(feature)
        threshold = float(threshold)
        if sample[feature] > threshold:  # 递归预测
            return self.__predict(sample, tree[root]['>' + str(round(float(threshold), 3))])
        else:
            return self.__predict(sample, tree[root]['<=' + str(round(float(threshold), 3))])


class AdaCost:
    def __init__(self, weak_classifier):
        self.__cost_matrix = '2'
        self.__weak_classifier = weak_classifier
        self.__weak_results = None
        self.__alpha_list = None

    def apply_weights_to_samples(self, X, y, weights):
        min_weights = weights.min().item()  # 记录最小权重
        new_X = torch.empty(0, X.size()[1], dtype=torch.long)  # empty
        new_y = torch.empty(0, dtype=torch.long)
        for i in range(len(X)):
            # 最小权重样本数为1，权重大的样本对应重复math.ceil(float(array(weiths.T)[0][i]/min_weights))次
            # repeat times for current sample
            times = int(math.ceil(float(weights[i].item() / min_weights)))
            new_X = torch.cat((new_X, X[i].unsqueeze(0).repeat(times, 1)), dim=0)
            new_y = torch.cat((
                new_y, y[i].unsqueeze(0).repeat(5)))
            # new_y.extend(y[i].item() for i in range(0, times))
        # new_y = torch.tensor(new_y)

        return new_X, new_y

    def train(self, X, y, max_iter=1):
        weekCartClassList = []
        n_samples = len(X)
        weights = torch.full((n_samples,), 1.0 / n_samples, dtype=torch.float64)  # 初始化所有样本的权重为1/m
        # final_predict_result = torch.zeros_like(y)
        self.__alpha_list = torch.empty(0, dtype=torch.float64)
        # 一行代表一次迭代的预测结果
        self.__weak_results = torch.empty(0, y.size()[0], dtype=torch.long)
        for i in range(max_iter):
            # bestWeekClass, bestPredictValue, error = CartTreeModel(X, y, weights, max_depth) #得到当前最优的弱分类器
            self.__weak_classifier.clear()
            self.__weak_classifier.train(X, y)
            tree_error_list, tree_predict_result = self.__weak_classifier.validate(X, y)
            # bestWeekClass = {}
            # bestWeekClass['cart'] = weak_classifier.get_model()
            e = (weights * tree_error_list).sum()  # correct: 0, wrong: 1
            alpha = 0.5 * torch.log((1.0 - e) / max(e, 1e-16))
            self.__alpha_list = torch.cat((self.__alpha_list, alpha.unsqueeze(0)))
            # bestWeekClass['alpha'] = alpha
            e_new = e * -2 + 1  # correct: 1, wrong: -1
            weights = weights * torch.exp(-1.0 * alpha * e_new)
            weights = weights / weights.sum()
            self.__weak_results = torch.cat((self.__weak_results,
                                             tree_predict_result.unsqueeze(0)),
                                            dim=0)
            # if errorRate == 0.0: break
        print("training done")
        return "training done"

    def validate(self, X, y):
        final_predict_result = torch.empty(0, dtype=torch.long)
        for sample_i in range(len(X)):
            stats = {}
            for weak_result_i in range(len(self.__weak_results)):
                weak_result = self.__weak_results[weak_result_i, sample_i].item()
                if weak_result not in stats.keys():
                    stats[weak_result] = 0
                stats[weak_result] += 1
            final_predict_result = torch.cat((
                final_predict_result, torch.tensor([max(stats, key=stats.get)])))
        print(final_predict_result)
        final_error = torch.eq(y, final_predict_result)
        error_rate = (len(X) - final_error.sum().item()) / len(X)
        print("total error: ", error_rate)
        # bestWeekClass['error_rate'] = error_rate
        # weekCartClassList.append(bestWeekClass)
        return


df = pandas.read_csv(r"C:\Users\chend\Desktop\Book1.csv", encoding='utf-8', index_col=False)
a = df[['dim1', 'dim2', 'dim3']]
b = df['y']
X = torch.from_numpy(a.values)
y = torch.from_numpy(b.values)

model = AdaCost(weak_classifier=CartTree(max_depth=3))
model.train(X, y, 10)
model.validate(X, y)

model2 = CartTree(max_depth=3)
model2.train(X, y)
errorList, predictResult = model2.validate(X, y)

print(errorList, predictResult)
