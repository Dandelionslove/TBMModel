<template>
	<el-container>
		<el-header width="100%" height="55px">掘进参数预测模型</el-header>

		<el-main width="100%">
			<el-tabs class="main_tabs" type="border-card">
				<el-tab-pane label="模型介绍" width="100%">
					<div></div>
				</el-tab-pane>
				<el-tab-pane label="模型算法" width="100%">
					<div></div>
				</el-tab-pane>
				<el-tab-pane label="模型测试" width="100%">
					<!-- 三个按钮 -->
					<el-row :gutter="20">
						<el-col :span="4">
							<el-upload class="upload-demo" :on-change="testUpload" accept=".csv" :limit="1" action="">
								<el-button type="warning" round>上传可用测试集</el-button>
							</el-upload>
						</el-col>
						<el-col :span="4">
							<el-button type="primary" @click="randomData()" round>随机更换测试数据</el-button>
						</el-col>
						<el-col :span="4">
							<el-button type="success" round>进行测试</el-button>
						</el-col>
					</el-row>
					<!-- 表格 -->
					<el-table :data="testShowRandomData" :row-class-name="tableRowClassName" height="400px">
						<el-table-column
							v-for="(item,key,index) in testTableColumnProp[0]"
							:key="index"
							:prop="key"
							:label="key"
						></el-table-column>
						<el-table-column fixed="right" prop="result" label="实际结果"></el-table-column>
						<el-table-column fixed="right" prop="date" label="测试结果"></el-table-column>
					</el-table>
				</el-tab-pane>
				<el-tab-pane label="模型使用" width="100%">
					<el-tabs>
						<el-tab-pane label="手动输入" name="first">
							<el-row :gutter="50">
								<!-- 参数列 -->
								<el-col :span="14">
									<el-form label-position="right" label-width="30%" :model="ManualForm">
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
											<el-button type="primary" @click="handleManualSubmit">获得预测值</el-button>
										</el-form-item>
									</el-form>
								</el-col>
								<!-- 结果列 -->
								<el-col :span="10">
									<el-table :data="MaunalResult">
										<el-table-column v-for="(item,key,index) in MaunalResult[0]" :key="index" :prop="key"></el-table-column>
									</el-table>
								</el-col>
							</el-row>
						</el-tab-pane>
						<el-tab-pane label="文档输入" name="second">
							<el-row>
								<el-col :span="4">
									<el-upload
										class="upload-doc"
										:on-change="modelApplication_upload"
										accept=".csv"
										:limit="1"
										action=""
									>
										<el-button type="success" round>上传文档(csv)</el-button>
									</el-upload>
								</el-col>
								<el-col :span="4">
									<el-button type="warning" round>开始预测(csv)</el-button>
								</el-col>
							</el-row>
							<el-table :data="modelApplication" height="330px" style="width: 100%">
								<el-table-column
									v-for="(item,key,index) in modelApplication[0]"
									:key="index"
									:prop="key"
									:label="key"
								></el-table-column>
								<el-table-column fixed="right" prop="F" label="F结果"></el-table-column>
								<el-table-column fixed="right" prop="T" label="T结果"></el-table-column>
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
</style>

<script>
export default {
	data() {
		return {
			testAllData: [],
			testShowRandomData: [],
			modelApplication: [],
			testTableColumnProp: [],
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
				input14: "58.925172019680400",
			},
		};
	},

	methods: {
		testUpload: function(obj, obj2) {
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
						dataRow[headers[j]] = temp[j];
						if (i == 1 && headers[j] != "result") {
							testTableColumnPropRow[headers[j]] = "1";
						}
					}
					testTableColumnPropList.push(testTableColumnPropRow);
					dataList.push(dataRow);
				}
			};

			this.testAllData = dataList;
			this.testTableColumnProp = testTableColumnPropList;
			// randomData();
		},
		randomData: function() {
			if (this.testAllData.length == 0) {
				this.$message({
					message: "请先上传数据集！",
					type: "warning"
				});
				return;
			}
			var randoms = [];
			while (true) {
				var isExists = false;
				var random = parseInt(Math.random() * this.testAllData.length);
				var index = jQuery.inArray(random, randoms);
				if (index < 0) randoms.push(random);
				if (randoms.length === 10) break;
			}
			var dataList = [];
			for (var i = 0; i < this.testAllData.length; i++) {
				var index = jQuery.inArray(i, randoms);
				if (index >= 0) {
					dataList.push(this.testAllData[i]);
				}
			}
			this.testShowRandomData = dataList;
		},

		handleManualSubmit: function() {
			// console.log(this.ManualForm);
			// this.$axios
			// 	.post('http://127.0.0.1:8000/api/RF_para', {
			// 		data: this.ManualForm,
			// 	})
			// 	.then(function(response) {
			// 		// this.MaunalResult
			// 		console.log(response);
			// 	})
			// 	.catch(function(error) {
			// 		console.log(error);
			// 	});
			this.$axios({
				url: 'http://127.0.0.1:8000/api/RF_para',
				methods: 'post',
				params: {
					'data': this.ManualForm
				},
			}).then(res => {
				this.MaunalResult[0].value = res.data[0];
				this.MaunalResult[1].value = res.data[1];
			}).catch(err => {
				alert(err);
			})
		},

		modelApplication_upload: function(obj, obj2) {
			var reader = new FileReader();
			reader.readAsText(obj.raw);
			var dataList = [];

			reader.onload = function() {
				var csvarry = this.result.split("\r\n");
				var headers = csvarry[0].split(",");
				for (var i = 1; i < csvarry.length; i++) {
					var dataRow = {};
					var temp = csvarry[i].split(",");
					for (var j = 0; j < temp.length; j++) {
						dataRow[headers[j]] = temp[j];
					}
					dataList.push(dataRow);
				}
			};
			this.modelApplication = dataList;
		},

		tableRowClassName({ row, rowIndex }) {
			if (rowIndex === 5) {
				return "warning-row";
			}
			// } else if (rowIndex === 3) {
			// 	return "success-row";
			// }
			return "success-row";
			return "";
		},

		handleExceed: function () {

		}
	}
};
</script>