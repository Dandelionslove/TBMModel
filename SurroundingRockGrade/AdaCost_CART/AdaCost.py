from sklearn.ensemble import AdaBoostClassifier
import numpy as np


class AdaCostClassifier(AdaBoostClassifier):
    # Add a private member __cost_matrix
    def __init__(self,
                 base_estimator=None,
                 n_estimators=50,
                 learning_rate=1.,
                 algorithm='SAMME.R',
                 random_state=None,
                 cost_matrix=None):

        super().__init__(
            base_estimator=base_estimator,
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=random_state)

        self.algorithm = algorithm
        self.__cost_matrix = cost_matrix

    def _boost_discrete(self, iboost, X, y, sample_weight, random_state):
        """Implement a single boost using the SAMME discrete algorithm."""
        estimator = self._make_estimator(random_state=random_state)

        estimator.fit(X, y, sample_weight=sample_weight)

        y_predict = estimator.predict(X)

        if iboost == 0:
            self.classes_ = getattr(estimator, 'classes_', None)
            self.n_classes_ = len(self.classes_)

        # Instances incorrectly classified
        incorrect = y_predict != y

        # Error fraction
        estimator_error = np.mean(
            np.average(incorrect, weights=sample_weight, axis=0))

        # Stop if classification is perfect
        if estimator_error <= 0:
            return sample_weight, 1., 0.

        n_classes = self.n_classes_

        # Stop if the error is at least as bad as random guessing
        if estimator_error >= 1. - (1. / n_classes):
            self.estimators_.pop(-1)
            if len(self.estimators_) == 0:
                raise ValueError('BaseClassifier in AdaBoostClassifier '
                                 'ensemble is worse than random, ensemble '
                                 'can not be fit.')
            return None, None, None

        # Boost weight using multi-class AdaBoost SAMME alg
        estimator_weight = self.learning_rate * (
            np.log((1. - estimator_error) / estimator_error) +
            np.log(n_classes - 1.))

        # Only boost the weights if I will fit again
        if not iboost == self.n_estimators - 1:
            # print("=====================================")
            # print("第",iboost,"次迭代：！！！！！！")
            # Only boost positive weights
            # print("第一部分")

            # print(estimator_weight * incorrect *
            #                         ((sample_weight > 0) |
            #                          (estimator_weight < 0)))
            # print("第二部分")
            # print(self._cost(y, y_predict))
            sample_weight *= np.exp(estimator_weight * incorrect *
                                    ((sample_weight > 0) |
                                     (estimator_weight < 0))
                                    * self._cost(y, y_predict)
                                    ) # 在原来的基础上乘以self._beta(y, y_predict)，即代价调整函数
            # print(estimator_weight * incorrect *
            #                         ((sample_weight > 0) |
            #                          (estimator_weight < 0))
            #                         * self._cost(y, y_predict)
            #                         )
        return sample_weight, estimator_weight, estimator_error


    #  新定义的代价调整函数
    def _cost(self, y, y_hat):
        res = []
        for i in zip(y, y_hat):
            res.append(self.__cost_matrix[i[1]][i[0]])
        #     if i[0] == i[1]:
        #         res.append(0)   # 正确分类
        #     elif i[0] == 2: # 真实II级
        #         if i[1] == 3: res.append(4)
        #         elif i[1] == 4: res.append(2)
        #         elif i[1] == 5: res.append(1)
        #         else:
        #             res.append(1)
        #
        #     elif i[0] == 3:  # 真实III级
        #         if i[1] == 2:
        #             res.append(1)
        #         elif i[1] == 4:
        #             res.append(2)
        #         elif i[1] == 5:
        #             res.append(1)
        #         else:
        #             res.append(1)
        #
        #     elif i[0] == 4: # 真实IV级
        #         if i[1] == 2: res.append(2)
        #         elif i[1] == 3: res.append(4)
        #         elif i[1] == 5: res.append(1)
        #         else:
        #             res.append(1)
        #
        #     elif i[0] == 5: # 真实V级
        #         if i[1] == 2: res.append(2)
        #         elif i[1] == 3: res.append(6)
        #         elif i[1] == 4: res.append(4)
        #         else:
        #             res.append(1)
        #     else:
        #         res.append(1)
        # # print(res)
        return np.array(res)

