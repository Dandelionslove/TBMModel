<template>
	<el-container>
		<el-header width="100%" height="55px">围岩等级预测模型</el-header>

		<el-main width="100%">
			<el-tabs class="main_tabs" type="border-card">
				<el-tab-pane label="模型介绍" width="100%">
					<div>本部分利用4393个循环段的稳定段掘进参数数据，首次将对代价敏感的AdaCost算法引入到围岩等级的预测中，以期帮助TBM司机判断周围的地质条件，为司机决策提供参考。</div>
					<h4></h4>
					<div>选择的特征重要性较大的参数主要包含以下10个：刀盘转速电位器值、刀盘运行时间、撑靴压力、刀盘转速、撑靴泵压力、左撑靴俯仰角、控制泵压力、右撑靴俯仰角、撑靴滚动角和撑靴油缸行程检测。</div>
					<h4></h4>
					<div>本文采用的围岩等级数据是由现场工程师根据现场条件，按照《水利水电工程地质勘察规范》得到。整个数据集。其中，III级岩体样本数量与V级岩体样本数量比值达到了240：1，存在明显的分类样本不均衡现象。由于在实际工程中，各类岩体级别误判的代价往往是不同的，同时为了提高不均衡数据中少数类样本（如V级岩体）的识别正确率，使用图示的代价矩阵。</div>

					<el-carousel height="350px" indicatorPosition="outside" ref="carousel">
						<el-carousel-item class="carousel-item" v-for="item in imgs" v-bind:key="item.url">
							<img class="carousel-img" :src="item.url" />
						</el-carousel-item>
					</el-carousel>
				</el-tab-pane>
				<el-tab-pane label="模型算法" width="100%">
					<h4>AdaCost算法是一种高效的代价敏感分类算法，可以有效的解决分类器倾向于将大部分样本识别为多数类样本的属性值，而导致少数类样本分类错误率较高的问题。</h4>
					<h4></h4>
					<div>AdaCost算法以CART树为弱分类器，通过多次迭代训练新的弱分类器更新样本权重，最终加权各个分类器分类结果得到模型的最终输出结果。在每次迭代过程中，AdaCost算法使用整个训练集来训练一个分类器，并根据模型分类结果正确与否与代价矩阵相应元素的取值，更新样本的权重。其更新策略为正确分类样本权重降低，错误分类样本权重增大；少数类样本权重增加的快，多数类样本权重增加的慢。由于CART树以最小化代价函数为准则划分样本，因此在模型下一次迭代训练时，误分类的少数类样本就被给予更多的关注，而使得AdaCost算法适用于不均衡数据分类问题的研究。</div>
					<h4></h4>
					<a href="https://www.cnblogs.com/kamekin/p/9906466.html">点击查看详细算法说明</a>
				</el-tab-pane>
				<el-tab-pane label="模型测试" width="100%">
					<!-- 三个按钮 -->
					<el-row :gutter="20">
						<el-col :span="4">
							<el-upload
								class="upload-demo"
								:on-error="handleModelTestUpload"
								accept=".csv"
								:limit="1"
								action
							>
								<el-button type="warning" round>上传可用测试集</el-button>
							</el-upload>
						</el-col>
						<el-col :span="4">
							<el-button type="primary" @click="randomData()" round>随机更换测试数据</el-button>
						</el-col>
						<el-col :span="4">
							<el-button type="success" round @click="handleModelTestSubmit">进行测试</el-button>
						</el-col>
					</el-row>
					<!-- 表格 -->
					<el-table
						:data="modelTestRandomShowingData"
						:row-class-name="tableRowClassName"
						height="400px"
					>
						<el-table-column
							v-for="(item,key,index) in modelTestTableColumnNameWithoutResult[0]"
							:key="index"
							:prop="key"
							:label="key"
						></el-table-column>
						<el-table-column fixed="right" prop="grade" label="实际结果"></el-table-column>
						<el-table-column fixed="right" prop="grade_predict" label="测试结果"></el-table-column>
					</el-table>
				</el-tab-pane>
				<el-tab-pane label="模型使用" width="100%">
					<el-tabs>
						<el-tab-pane label="手动输入" name="first">
							<el-row>
								<!-- 参数列 -->
								<el-form label-position="right" label-width="20%" :model="ManualForm">
									<el-form-item label="刀盘运行时间均值">
										<el-input v-model="ManualForm.cutterHeadRunTimeMean" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="撑靴压力均值">
										<el-input v-model="ManualForm.shoePressureMean" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="刀盘转速均值">
										<el-input v-model="ManualForm.cutterHeadSpeedMean" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="撑靴泵压力均值">
										<el-input v-model="ManualForm.shoePumpPressureMean" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="左撑靴俯仰角均值">
										<el-input v-model="ManualForm.leftShoePitchAngleMean" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="控制泵压力均值">
										<el-input v-model="ManualForm.controlPumpPressureMean" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="右撑靴俯仰角均值">
										<el-input v-model="ManualForm.RightShoePitchAngleMean" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="左撑靴滚动角均值">
										<el-input v-model="ManualForm.leftShoeRollAngleMean" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="左撑靴油缸行程检测均值">
										<el-input v-model="ManualForm.leftShoeCylinderStrokeMean" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="右撑靴滚动角均值">
										<el-input v-model="ManualForm.RightShoeRollAngleMean" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="右撑靴油缸行程检测均值">
										<el-input v-model="ManualForm.RightShoeCylinderStrokeMean" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item>
										<el-button type="primary" @click="handleModelApplyManualSubmit">获得预测值</el-button>
									</el-form-item>
								</el-form>
							</el-row>
							<!-- 结果列 -->
							<el-row>
								<el-table :data="MaunalResult" class="result">
									<el-table-column v-for="(item,key,index) in MaunalResult[0]" :key="index" :prop="key"></el-table-column>
								</el-table>
							</el-row>
						</el-tab-pane>
						<el-tab-pane label="文档输入" name="second">
							<el-row>
								<el-col :span="4">
									<el-upload class="upload-doc" :on-error="handleModelApplyUpload" accept=".txt" :limit="1" action>
										<el-button type="success" round>上传文档(txt)</el-button>
									</el-upload>
								</el-col>
								<el-col :span="4">
									<el-button type="warning" round @click="handleModelApplyBatchSubmit">开始预测</el-button>
								</el-col>
							</el-row>
							<el-table :data="modelApplyAllData" height="330px" style="width: 100%">
								<el-table-column
									v-for="(item,key,index) in modelApplyAllData[0]"
									:key="index"
									:prop="key"
									:label="key"
								></el-table-column>
								<el-table-column fixed="right" prop="grade_predict" label="围岩等级结果"></el-table-column>
							</el-table>
						</el-tab-pane>
					</el-tabs>
				</el-tab-pane>
			</el-tabs>
		</el-main>
	</el-container>
</template>



<style>
.el-header {
	line-height: 60px;
	background: #303133;
	width: 100%;
	color: #ddd8d8;
}
.main_tabs {
	margin-top: 0px;
	height: 100%;
	width: 100%;
	overflow: auto;
	/* position: relative; */
	/* top: 0px;
    left: 0px; */
}
.el-container {
	height: 100%;
	width: 100%;
}
.carousel-item {
	width: 100%;
	height: 100%;
	background: white;
	display: flex;
	justify-content: center;
}
  .carousel-img {
	max-width: 100%;
	max-height: 100%;
}
.el-form {
	width: 80%;
	margin: auto;
}

.result {
	width: 40%;
	margin: auto;
}
.el-table .warning-row {
	background: rgb(240, 174, 174);
}

.el-table .success-row {
	background: #f0f9eb;
}
</style>

<script>
import JSZip from "jszip";

export default {
	data() {
		return {
			modelTestAllUploadData: [],
			modelTestRandomShowingData: [],
			modelApplyAllData: [],
			modelTestTableColumnNameWithoutResult: [],
			MaunalResult: [
				{
					variable: "rock_grade",
					value: null
				}
			],
			ManualForm: {
				cutterHeadRunTimeMean: "1",
				shoePressureMean: "1",
				cutterHeadSpeedMean: "1",
				shoePumpPressureMean: "1",
				leftShoePitchAngleMean: "1",
				controlPumpPressureMean: "1",
				RightShoePitchAngleMean: "1",
				leftShoeRollAngleMean: "1",
				leftShoeCylinderStrokeMean: "1",
				RightShoeRollAngleMean: "1",
				RightShoeCylinderStrokeMean: "1"
			},
			imgs: [
				{ url: require("../assets/adacost1.png"), link: "/content1" },
				{ url: require("../assets/adacost2.png"), link: "/content2" },
				{ url: require("../assets/logo.png"), link: "/content3" }
			],
			modelTestResult: []
		};
	},

	methods: {
		handleModelTestUpload: function(err, obj, fileList) {
			var reader = new FileReader();
			reader.readAsText(obj.raw);
			var dataList = [];
			var testTableColumnPropList = [];
			reader.onload = function() {
				var csvarry = this.result.split("\r\n");
				var headers = csvarry[0].split(",");
				for (var i = 1; i < csvarry.length; i++) {
					var dataRow = {};
					var testTableColumnPropRow = {};
					var temp = csvarry[i].split(",");
					for (var j = 0; j < temp.length; j++) {
						if (headers[j] != "index") {
							dataRow[headers[j]] = temp[j];
						}
						if (i == 1 && headers[j] != "grade" && headers[j] != "index") {
							testTableColumnPropRow[headers[j]] = "1";
						}
					}
					testTableColumnPropList.push(testTableColumnPropRow);
					dataList.push(dataRow);
				}
			};

			this.modelTestAllUploadData = dataList;
			this.modelTestTableColumnNameWithoutResult = testTableColumnPropList;
			// randomData();
			this.$message({
				message: "上传成功，请点击随即更换测试数据",
				type: "success"
			});
		},
		randomData: function() {
			if (this.modelTestAllUploadData.length == 0) {
				this.$message({
					message: "请先上传数据集！",
					type: "warning"
				});
				return;
			}
			var randoms = [];
			while (true) {
				var isExists = false;
				var random = parseInt(
					Math.random() * this.modelTestAllUploadData.length
				);
				var index = jQuery.inArray(random, randoms);
				if (index < 0) randoms.push(random);
				if (randoms.length === 10) break;
			}
			var dataList = [];
			for (var i = 0; i < this.modelTestAllUploadData.length; i++) {
				var index = jQuery.inArray(i, randoms);
				if (index >= 0) {
					dataList.push(this.modelTestAllUploadData[i]);
				}
			}
			this.modelTestRandomShowingData = dataList;
		},
		handleModelTestSubmit: function() {
			if (this.modelTestAllUploadData.length == 0) {
				this.$message({
					message: "请先上传数据集！",
					type: "warning"
				});
				return;
			}
			// 去除已经有的两列结果
			var tableToBeSubmited = [];
			var tableToBeSubmited = this.modelTestRandomShowingData.map(
				this.modifyTableDataToBeSubmited
			);
			let t = this;
			var resultList = [];

			this.$axios({
				url: "http://127.0.0.1:8000/api/AC_batch",
				methods: "get",
				params: {
					data: JSON.stringify(tableToBeSubmited)
				}
			})
				.then(res => {
					// 异步
					resultList = res["data"];
					//给modelTestRandomShowingData加一列结果
					var temp = [];
					// console.log(resultList);
					this.modelTestRandomShowingData.forEach((value, index) => {
						temp[index] = value;
						temp[index]["grade_predict"] = resultList[index];
					});
					this.$message({
						message: "结果已出",
						type: "success"
					});
					t.modelTestRandomShowingData = temp;
				})
				.catch(err => {
					alert(err);
				});

			// console.log(this.modelTestRandomShowingData);
		},
		modifyTableDataToBeSubmited: function(value, index, array) {
			var dataRow = [];
			for (var key in value) {
				if (key == "grade" || key == "grade_predict") continue;
				dataRow.push(value[key]);
			}
			return dataRow;
		},

		// handleZipUpload: function(response, file, fileList) {
		// 	this.zip = file;
		// },
		handleModelApplyBatchSubmit: function() {
			if (this.modelApplyAllData.length === 0) {
				this.$message({
					message: "请先上传数据集！",
					type: "warning"
				});
				return;
			}
			this.$axios({
				url: "http://127.0.0.1:8000/api/AC_file",
				methods: "post",
				params: {
					data: this.modelApplyAllData,
				}
			})
				.then(res => {
					alert(res);
				})
				.catch(err => {
					alert(err);
				});
		},
		// handleModelApplyBatchSubmit: function() {
		// 	if (this.modelApplyAllData.length == 0) {
		// 		this.$message({
		// 			message: "请先上传数据集！",
		// 			type: "warning"
		// 		});
		// 		return;
		// 	}
		// 	// 去除已经有的两列结果
		// 	var tableToBeSubmited = [];
		// 	var tableToBeSubmited = this.modelApplyAllData.map(
		// 		this.modifyTableDataToBeSubmited
		// 	);
		// 	this.$axios({
		// 		url: "http://127.0.0.1:8000/api/adaCostBatch",
		// 		methods: "post",
		// 		params: {
		// 			data: tableToBeSubmited
		// 		}
		// 	})
		// 		.then(res => {
		// 			//给modelApplyAllData加一列
		// 		})
		// 		.catch(err => {
		// 			alert(err);
		// 		});
		// 	var temp = [];
		// 	this.modelApplyAllData.forEach(function(value, index) {
		// 		console.log(index);
		//
		// 		temp[index] = value;
		// 		temp[index]["grade_predict"] = 100;
		// 	});
		// 	this.modelApplyAllData = temp;
		// },
		handleModelApplyManualSubmit: function() {
			this.$axios({
				url: "http://127.0.0.1:8000/api/AC_para",
				methods: "get",
				params: {
					data: this.ManualForm
				}
			})
				.then(res => {
					// console.log(res["data"]);
					this.MaunalResult[0].value = res["data"][0];
					this.$message({
						message: "结果已出",
						type: "success"
					});
				})
				.catch(err => {
					alert(err);
				});
		},

		handleModelApplyUpload: function(err, obj, fileList) {
			var reader = new FileReader();
			reader.readAsText(obj.raw);
			reader.onload = function (evt) {
				this.modelApplyAllData = evt.target.result;
			};
			// var reader = new FileReader();
			// reader.readAsText(obj.raw);
			// var dataList = [];
			//
			// reader.onload = function() {
			// 	var csvarry = this.result.split("\r\n");
			// 	var headers = csvarry[0].split(",");
			// 	for (var i = 1; i < csvarry.length; i++) {
			// 		var dataRow = {};
			// 		var temp = csvarry[i].split(",");
			// 		for (var j = 0; j < temp.length; j++) {
			// 			dataRow[headers[j]] = temp[j];
			// 		}
			// 		dataList.push(dataRow);
			// 	}
			// };
			// this.modelApplyAllData = dataList;
		},

		tableRowClassName({ row, rowIndex }) {
			if (row["grade_predict"] == null) return "";
			if (row["grade"] == row["grade_predict"]) {
				return "success-row";
			}
			return "warning-row";
		},

		handleExceed: function() {}
	}
};
</script>
