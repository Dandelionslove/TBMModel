<template>
	<el-container width="100%">
		<el-header width="100%" height="55px">数据示例</el-header>

		<el-main width="100%" height="300px">
			<h4>TBM[Tunnel Boring Machine，隧道掘进机]施工涉及多专业、多工艺，掘进信息类型多元、关系复杂，不仅包括了地质信息、岩体信息、设备机电液参数、维保记录、风险预警等原始信息，还包括了由设备和岩体相互作用的衍生数据。</h4>
			<h4>TBM设备整体的数字化程度较高，超过300只传感器分布于设备各个功能单元。此外，TBM辅助功能系统如导向系统、皮带机输碴系统、支护系统等参数也集成传输到上位机电脑中。</h4>
			<h4>TBM每1-10 s会自动采集并存储一次盾构工作中的数据。TBM施工过程中的各种数据，如设备维保、刀具更换、材料消耗、地层加固等信息一般由一线人员记录，通过权限登录信息平台客户端，按既定规则上传至相应数据库中。此外，现场实验数据、监测数据、照片、视频等任意格式信息文件都可通过客户端上传至中心服务器数据库中，完成信息的全面收集和保存。</h4>

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