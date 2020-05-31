<template>
	<el-container>
		<el-header width="100%" height="55px">掘进参数预测模型</el-header>

		<el-main width="100%">
			<el-tabs class="main_tabs" type="border-card">
				<el-tab-pane label="模型介绍" width="100%">
					<div>本部分在数据预处理的基础上，对4393个TBM掘进循环上升段和稳定段的199种掘进参数进行了特征选择，进而对TBM掘进过程中稳定段的总推进力F和刀盘扭矩T进行预测，以期为TBM司机驾驶设定参数提供有效的参考。</div>
					<div>掘进过程产生的掘进参数共有199种，在众多参数中选取对F和T有较大影响的掘进参数是一项必要工作。本文采取上述基于RF的特征变量重要性算法，结合TBM上升段前30 s与稳定段数据选取对掘进变量预测有利的参数</div>
					<el-carousel height="350px" indicatorPosition="outside" ref="carousel">
						<el-carousel-item class="carousel-item" v-for="item in imgs" v-bind:key="item.url">
							<img class="carousel-img" :src="item.url" />
						</el-carousel-item>
					</el-carousel>
				</el-tab-pane>
				<el-tab-pane label="模型算法" width="100%">
					<h4>随机森林（RF）是一种基于CART决策树的集成算法，可应用于分类与回归问题。研究表明RF算法对多元共线变量不敏感，具有较高的预测准确率，对异常值和噪声有较好的容忍度，且不容易出现过拟合，是机器学习十大算法之一。</h4>
					<h4></h4>
					<div>RF通过随机选择训练样本与随机选择特征变量的方法生成多棵CART决策树，并将这些树的决策结果组合并投票或取均值，得到的最终分类或回归的结果可以较好的克服单棵决策树泛化能力较差的缺点。具体而言，如图4所示，RF在生成CART树的过程中，主要采用bootstrap重抽样方法按每次2/3的比例从原始数据集中抽取k个样本分别作为k棵CART树的训练数据。这k个样本称为袋内（In Bag）数据，而每次未被抽中的约1/3的数据称为袋外（Out of Bag, OOB）数据，RF利用OOB进行内部误差估计，以提升模型的泛化能力。由于bootstrap采用独立随机重抽样的方式，支持并行运算，运算速度仅由单棵最大深度决策树的计算时间制约，计算速度快；且使用重抽样的方法达到样本空间重构的效果，使得k棵CART树的训练样本不尽相同，减少k棵树之间的相关性。此外RF还会从所有M个变量中按一定比随机选取m个作为每棵CART树训练的特征变量，进一步减小生成k棵树之间的相关性，从而提高整个集成模型的性能。</div>
					<h4></h4>
					<a href="https://blog.csdn.net/qq_32607273/article/details/81940528">点击查看详细算法说明</a>
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
								action=""
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
						<el-table-column fixed="right" prop="F" label="F实际结果"></el-table-column>
						<el-table-column fixed="right" prop="T" label="T实际结果"></el-table-column>
						<el-table-column fixed="right" prop="F_predict" label="F测试结果"></el-table-column>
						<el-table-column fixed="right" prop="T_predict" label="T测试结果"></el-table-column>
					</el-table>
				</el-tab-pane>
				<el-tab-pane label="模型使用" width="100%">
					<el-tabs>
						<el-tab-pane label="手动输入" name="first">
							<el-row>
								<!-- 参数列 -->
								<el-form label-position="right" label-width="20%" :model="ManualForm">
									<el-form-item label="总推进力均值">
										<el-input v-model="ManualForm.input1" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="总推进力方差">
										<el-input v-model="ManualForm.input2" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="刀盘功率均值">
										<el-input v-model="ManualForm.input3" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="刀盘功率方差">
										<el-input v-model="ManualForm.input4" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="刀盘扭矩均值">
										<el-input v-model="ManualForm.input5" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="刀盘扭矩方差">
										<el-input v-model="ManualForm.input6" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="推进速度均值">
										<el-input v-model="ManualForm.input7" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="推进速度方差">
										<el-input v-model="ManualForm.input8" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="刀盘速度给定均值">
										<el-input v-model="ManualForm.input9" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="刀盘速度给定方差">
										<el-input v-model="ManualForm.input10" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="刀盘转速均值">
										<el-input v-model="ManualForm.input11" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="刀盘转速方差">
										<el-input v-model="ManualForm.input12" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="稳定段刀盘转速均值">
										<el-input v-model="ManualForm.input13" placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="稳定段推进速度均值">
										<el-input v-model="ManualForm.input14" placeholder="请输入内容"></el-input>
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
									<el-button type="warning" round @click="handleModelApplyFileSubmit">开始预测</el-button>
								</el-col>
								<el-col :span="4">
									<el-button type="primary" round @click="getFileResult">获得结果</el-button>
								</el-col>
							</el-row>
							<el-table :data="fileResult" height="330px" style="width: 100%">
								<el-table-column
									v-for="(item,key,index) in fileResult_header[0]"
									:key="index"
									:prop="key"
									:label="key"
								></el-table-column>
								<el-table-column fixed="right" prop="F_predict" label="F结果"></el-table-column>
								<el-table-column fixed="right" prop="T_predict" label="T结果"></el-table-column>
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
</style>

<script>
	import $ from 'jquery';

export default {
	data() {
		return {
			modelTestAllUploadData: [],
			modelTestRandomShowingData: [],
			modelApplyAllData: [],
			fileResult: [],
			fileResult_header: [],
			modelTestTableColumnNameWithoutResult: [],
			MaunalResult: [
				{
					variable: "T",
					value: null
				},
				{
					variable: "F",
					value: null
				}
			],
			ManualForm: {
				input1: "9884.709148247640",
				input2: "4282792.478886330",
				input3: "580.2759022011320",
				input4: "106839.89906191500",
				input5: "1016.0895842466500",
				input6: "230300.9990925620",
				input7: "12.27173775565610",
				input8: "72.42625214652270",
				input9: "6927.610487980730",
				input10: "526175.9346199800",
				input11: "5.1681886625443200",
				input12: "0.326242984454731",
				input13: "7.216352884750970",
				input14: "58.925172019680400"
			},
			imgs: [
				{ url: require("../assets/rf1.png"), link: "/content1" },
				{ url: require("../assets/rf2.png"), link: "/content2" },
				{ url: require("../assets/logo.png"), link: "/content3" }
			]
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
						if (i == 1 && headers[j] != "F" && headers[j] != "T" && headers[j] != "index") {
							testTableColumnPropRow[headers[j]] = "1";
						}
					}
					testTableColumnPropList.push(testTableColumnPropRow);
					dataList.push(dataRow);
				}
			};

			this.modelTestAllUploadData = dataList;
			this.modelTestTableColumnNameWithoutResult = testTableColumnPropList;
			// this.randomData();
			this.$message({
				message: "上传成功，请点击随即更换测试数据",
				type: "success"
			});
		},
		randomData: function() {
			console.log(this.modelTestRandomShowingData);
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
			this.$axios({
				url: "http://127.0.0.1:8000/api/RF_batch",
				methods: "get",
				params: {
					data: JSON.stringify(tableToBeSubmited)
				}
			})
				.then(res => {
					// 异步
					var resultList = res["data"];

					console.log(resultList);
					//给modelTestRandomShowingData加2列
					var temp = [];
					this.modelTestRandomShowingData.forEach((value, index) => {
						temp[index] = value;
						temp[index]["F_predict"] = resultList[index][0];
						temp[index]["T_predict"] = resultList[index][1];
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
		},
		modifyTableDataToBeSubmited: function(value, index, array) {
			var dataRow = [];
			for (var key in value) {
				if (
					key == "F" ||
					key == "F_predict" ||
					key == "T" ||
					key == "T_predict"
				)
					continue;
				dataRow.push(value[key]);
			}
			return dataRow;
		},
		// handleZipUpload: function(response, file, fileList) {
		// 	this.zip = file;
		// },
		handleModelApplyFileSubmit: function() {
			if (this.modelApplyAllData.length === 0) {
				this.$message({
					message: "请先上传数据集！",
					type: "warning"
				});
				return;
			}

			let _this = this;
			for (let i = 0; i < _this.modelApplyAllData.length; i++)
			{
				if (i < _this.modelApplyAllData.length-1) {
					setTimeout(function(i) {
						return function () {
							$.ajax({
								url: "http://127.0.0.1:8000/api/RF_file",
								type: "GET",
								async: false,
								data: {
									length: JSON.stringify(_this.modelApplyAllData.length),
									count: JSON.stringify(i),
									data: JSON.stringify(_this.modelApplyAllData[i]),
								},
								timeout:5000,
								dataType:'json',
								error: function (err) {
									console.log(err);
								}
							})
						}
					}(i), 10);
				}
				else
				{
					setTimeout(function(i) {
						return function () {
							$.ajax({
								url: "http://127.0.0.1:8000/api/RF_file",
								type: "GET",
								async: false,
								data: {
									length: JSON.stringify(-1),
									count: JSON.stringify(-1),
									data: JSON.stringify(_this.modelApplyAllData[i]),
								},
								timeout:5000,
								dataType:'json',
								error: function (err) {
									console.log(err);
								}
							})
						}
					}(i), 10);
				}
			}
			// let promiseList = [];
			// for (let i = 0; i < _this.modelApplyAllData.length; i++)
			// {
			// 	let p1 = new Promise(function (resolve, reject) {
			// 		_this.$axios({
			// 			url: "http://127.0.0.1:8000/api/RF_file",
			// 			methods: "get",
			// 			async: false,
			// 			params: {
			// 				length: JSON.stringify(_this.modelApplyAllData.length),
			// 				count: JSON.stringify(i),
			// 				data: JSON.stringify(_this.modelApplyAllData[i]),
			// 			}
			// 		})
			// 			.then(res => {
			// 				resolve(res);
			// 			})
			// 			.catch(err => {
			// 				reject(err);
			// 			});
			// 	});
			// 	promiseList.push(p1);
			// }
			// console.log(promiseList);
			// Promise.all(promiseList).then(function () {
			// 	_this.$axios({
			// 		url: "http://127.0.0.1:8000/api/RF_file",
			// 		methods: "get",
			// 		params: {
			// 			length: JSON.stringify(-1),
			// 			count: JSON.stringify(-1),
			// 			data: JSON.stringify("$$$$$$$$$$"),
			// 		}
			// 	})
			// 		.then(res => {
			// 			console.log(res);
			// 		})
			// 		.catch(err => {
			// 			console.log(err);
			// 		});
			// });
		},
		
		handleModelApplyManualSubmit: function() {
			this.$axios({
				url: "http://127.0.0.1:8000/api/RF_para",
				methods: "post",
				params: {
					data: this.ManualForm
				}
			}).then(res => {
				this.MaunalResult[0].value = res.data[0];
				this.MaunalResult[1].value = res.data[1];
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
			// let _this = this;
			// var reader = new FileReader();
			// reader.readAsText(obj.raw);
			// reader.onload = function () {
			// 	_this.modelApplyAllData = this.result.substr(0, this.result.length/4);
			// };
			let reader = new FileReader();
			reader.readAsText(obj.raw);
			let _this = this;
			reader.onload = function() {
				let substr = this.result.substr(0, this.result.length);
				_this.modelApplyAllData = substr.split("\r\n");
				_this.modelApplyAllData.pop();
				_this.modelApplyAllData.push('$$$$$$$$$$');
				// console.log(_this.modelApplyAllData);
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
			// 		dataRow["predict_T"] = 0;
			// 		dataRow["predict_F"] = 0;
			// 		dataList.push(dataRow);
			// 	}
			// };
			// this.modelApplyAllData = dataList;
		},

		getFileResult: function() {
			this.$axios({
				url: "http://127.0.0.1:8000/api/RF_result",
				methods: "get",
			}).then(res => {
					var dataRow = {};
					var dataRow_header = {};
					var header_name = ['参数1','参数2','参数3','参数4','参数5','参数6','参数7',
					'参数8','参数9','参数10','参数11','参数12','参数13','参数14']
					for (var i = 0; i < res.data.prepro.length; i++) {
						dataRow[header_name[i]] = res.data.prepro[i];
						dataRow_header[header_name[i]] = res.data.prepro[i];
					}
					// 专门存放列名 去除结果列，为了让结果列单独固定显示
					var dataArr_header = [];
					dataArr_header.push(dataRow_header);
					this.fileResult_header = dataArr_header;

					// 
					dataRow["F_predict"] = res.data.result[0];
					dataRow["T_predict"] = res.data.result[1];
					var dataArr = [];
					dataArr.push(dataRow);
					this.fileResult = dataArr;
			})
				.catch(err => {
					alert(err);
				});
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