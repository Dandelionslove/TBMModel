<template>
	<el-container class="biggest">
		<!-- 侧边栏 -->
		<el-aside width="180px">
			<div id="menu"></div>
		</el-aside>

		<router-view width="85%"></router-view>
	</el-container>
</template>


<style>
.el-aside {
	background-color: #545c64;
}
.biggest {
	margin-top: 0px;
    height: 100%;
    position: absolute;
    top: 0px;
    left: 0px;
}

/* .el-aside {
	height: 100%;
	position: absolute;
	top: 0px;
	left: 0px;
	width: 20%;
}
.el-main {
	height: 100%;
	position: absolute;
	top: 0px;
	left: 250px;
	width: 80%;
} */
</style>

<script>
export default {
	date() {
		return {
			
		};
	}
};
</script>