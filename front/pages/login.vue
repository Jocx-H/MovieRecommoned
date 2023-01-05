<!--
@File   : login.vue
@Time   : 2023/1/1 14:41:04
@Author : Sparkling-Y
@Desc   : 登陆界面
-->

<template>
	<view>
		<!-- 图标 -->
		<view class="title">
			<image mode="widthFix" style="width: calc(35%);" src="../static/title.png">
			</image>
		</view>
		<!-- 账号 -->
		<view class="admin">
			<input class="uni-input" v-model="id" type="text" placeholder="account" placeholder-style="font-size:40rpx;color:#ACACAC;" />
		</view>
		<!-- 密码 -->
		<view class="pwd">
			<input class="uni-input"  v-model="password" password type="text" placeholder="password"  placeholder-style="font-size:40rpx;color:#ACACAC;"/>
		</view>
		<!-- 登录 -->
		<button class="log-btn" @click="log_in()">
			<text>sign in</text>
		</button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				id: "",
				password: "",
			}
		},
		methods: {
			log_in() {
				uni.request({
					url: 'http://82.156.202.134:23333/api/login/login?usr=' + this.id,
					method: 'POST',
					success: res => {
						if (res.data.result == true){
							uni.navigateTo({
								url:"./main?id=" + this.id,
							})
						}
							
					},
				})
				
			},
		}
	}
</script>

<style>	
	page{
		height: 100%;
		position: fixed;
		background-image: url(../static/bg.jpg);
	}
	@font-face{
		font-family: cute;
		src: url('~@/static/NoganasRegular-mL73m.ttf');
		@include flex;
		flex-direction: row;
		flex-wrap: wrap;
		align-items: center;
	}
	.title{
		margin-top: calc(13%);
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.admin{
		font-family: cute;
		margin-top:calc(5%);
		margin-left:calc(40%);
		margin-right:calc(40%);
		height: 70rpx;
		color: #d9d9d9;
		display: flex;
		align-items: center;
		justify-content: center;
		border: 5rpx solid #d9d9d9;
		/* border-radius: 20rpx; */
		/* padding: 10rpx; */
	}
	.pwd{
		font-family: cute;
		margin-top:calc(3%);
		margin-left:calc(40%);
		margin-right:calc(40%);
		height: 70rpx;
		color: #d9d9d9;
		display: flex;
		align-items: center;
		justify-content: center;
		border: 5rpx solid #d9d9d9;
		/* border-radius: 20rpx; */
		/* padding: 10rpx; */
	}
	.log-btn{
		font-family: cute;
		margin-top:calc(4%);
		margin-left:calc(45%);
		margin-right:calc(45%);
		margin-bottom:calc(2%);
		height: 90rpx;
		background-color: #ffffff;
		color: #000000;
		font-size: 45rpx;
		font-family: cute;
		line-height: 45px;
		/* border-radius: 20rpx; */
		/* box-shadow: 0px 3px 1px -2px rgba(0, 0, 0, 0.2), 0px 3px 2px 0px rgba(0, 0, 0, 0.15), 0px 1px 5px 0px rgba(0, 0, 0, 0.12); */
	}
	

	button{
		list-style: none;
		transition: .3s linear;
	}
	button:hover{
		background-color: #f1f1f1;
		transform: scale(1.1);
	}
	button::before, button::after{
	    position: absolute;
	    content: '';
	    transition: 1.1s ease-out ;
	}
</style>
