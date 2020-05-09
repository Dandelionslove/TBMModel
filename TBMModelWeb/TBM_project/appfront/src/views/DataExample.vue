<template>
	<el-container width="100%">
		<el-header width="100%" height="55px">数据示例</el-header>

		<el-main width="100%" height="300px">
			<h3>文字描述 Lorem ipsum dolor sit amet consectetur, adipisicing elit. Tempore alias repellendus odit ut, saepe error consectetur tenetur amet non fuga at labore voluptatibus modi maiores voluptatum soluta quod eius rerum!</h3>

			<!-- :action是执行上传动作的后台接口 -->
			<!-- el-button是触发上传的按钮 -->
			<!-- :on-exceed绑定的方法则是处理超出数量后的动作 -->
			<el-upload
				class="upload-demo"
				:on-change="handleChange"
				accept=".csv"
				:limit="1"
				:on-exceed="handleOnExecute"
				action=""
			>
				<el-button size="small" type="primary">点击上传</el-button>
			</el-upload>

			<h1></h1>

			<el-table :data="tableData" height="350px" border>
				<el-table-column v-for="(item,key,index) in tableData[0]" :key="index" :prop="key" :label="key"></el-table-column>
			</el-table>
		</el-main>
	</el-container>
</template>

<script>
export default {
	data() {
		return {
			tableData: []
		};
	},

	methods: {
		handleChange: function(obj, obj2) {
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
			this.tableData = dataList;
		},

		handleOnExecute: function () {

		}
	}
};
</script>


<style>
.el-header {
	line-height: 60px;
	background: #303133;
	width: 100%;
	color: #ddd8d8;
}
.el-container {
	margin-top: 0px;
    height: 100%;
    /* position: absolute; */
    top: 0px;
    left: 0px;
}
</style>