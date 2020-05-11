<template>
	<el-container>
		<el-header width="100%" height="55px">围岩等级预测模型</el-header>

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
							<el-upload class="upload-demo" :on-change="testUpload" accept=".csv" :limit="1" action>
								<el-button type="warning" round>上传可用测试集</el-button>
							</el-upload>
						</el-col>
						<el-col :span="4">
							<el-button type="primary" @click="randomData()" round>随机更换测试数据</el-button>
						</el-col>
						<el-col :span="4">
							<el-button type="success" round @click="handleBatchSubmit">进行测试</el-button>
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
										:on-change="modelApply_upload"
										accept=".csv"
										:limit="1"
										action
									>
										<el-button type="success" round>上传文档(csv)</el-button>
									</el-upload>
								</el-col>
								<el-col :span="4">
									<el-button type="warning" round>开始预测(csv)</el-button>
								</el-col>
							</el-row>
							<el-table :data="modelApplyAllData" height="330px" style="width: 100%">
								<el-table-column
									v-for="(item,key,index) in modelApplyAllData[0]"
									:key="index"
									:prop="key"
									:label="key"
								></el-table-column>
								<el-table-column fixed="right" prop="F" label="围岩等级结果"></el-table-column>
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
			modelApplyAllData: [],
			testTableColumnProp: [],
			MaunalResult: [
				{
					variable: "围岩等级",
					value: null
				}
            ],
            BatchResult_apply: [
				{
					variable: "围岩等级",
					value: null
				}
            ],
            BatchResult_test: [
				{
					variable: "围岩等级",
					value: null
				}
			],
			ManualForm: {
				cutterHeadRunTimeMean: "",
				shoePressureMean: "",
				cutterHeadSpeedMean: "",
				shoePumpPressureMean: "",
				leftShoePitchAngleMean: "",
				controlPumpPressureMean: "",
				RightShoePitchAngleMean: "",
				leftShoeRollAngleMean: "",
				leftShoeCylinderStrokeMean: "",
				RightShoeRollAngleMean: "",
				RightShoeCylinderStrokeMean: ""
			}
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
		handleBatchSubmit_test: function() {
			this.$axios({
				url: "http://127.0.0.1:8000/api/adaCostBatch",
				methods: "post",
				params: {
					data: this.testShowRandomData
				}
			})
				.then(res => {
					this.BatchResult_test = res[0];
				})
				.catch(err => {
					alert(err);
				});
        },
        handleBatchSubmit_apply: function() {
			this.$axios({
				url: "http://127.0.0.1:8000/api/adaCostBatch",
				methods: "post",
				params: {
					data: this.modelApplyAllData
				}
			})
				.then(res => {
					this.BatchResult_apply[0].value = res[0];
				})
				.catch(err => {
					alert(err);
				});
		},
		handleManualSubmit: function() {
			this.$axios({
				url: "http://127.0.0.1:8000/api/adaCostManual",
				methods: "post",
				params: {
					data: this.ManualForm
				}
			})
				.then(res => {
					this.MaunalResult[0].value = res[0];
				})
				.catch(err => {
					alert(err);
				});
		},

		modelApply_upload: function(obj, obj2) {
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
			this.modelApplyAllData = dataList;
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

		handleExceed: function() {}
	}
};
</script>