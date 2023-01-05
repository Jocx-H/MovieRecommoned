<!--
@File   : detail.vue
@Time   : 2022/1/2 ‏‎19:42:01
@Author : Sparkling-Y
@Desc   : 详情页
-->

<template>
	<view>
		<!-- 顶部导航栏 -->
		<view class="navi">
			<uni-row>
				<!-- title -->
				<uni-col :span="22">
					<view class="title" @click="navi_main()">
						<view style="cursor: pointer; width: calc(15%);">MOVIES</view>
					</view>
				</uni-col>
				<!-- 用户头像 -->
				<uni-col :span="2">
					<view class="portrait">
						<image style="text-decoration:none;height: 40px; width: 40px; display: block; margin: 0 auto;border-radius: 50%;  border: 3rpx solid #9f9f9f;" src="../static/portrait.png">
						</image>
					</view>
				</uni-col>
			</uni-row>
		</view>
		<image class="bg_img" src="../static/bg.jpg" mode="aspectFill"></image>
		<!-- 详情信息 -->
		<view class="detail-box">
			<!-- 封面 -->
			<image class="detail-img" :src="pic_path" mode="heightFix"></image>
			<!-- 详情信息 -->
			<view class="detail-info">
				<view class="detail-title">{{name}}</view>
				<view class="detail-left">Release Time</view>
				<view class="detail-left" style="margin-top: 35px;">Directors</view>
				<view class="detail-left" style="margin-top: 70px;">Writers</view>
				<view class="detail-left" style="margin-top: 105px;">Stars</view>
				<view class="detail-left" style="margin-top: 140px;">Introduction</view>
				<view class="detail-left" style="bottom: 190px;">Rate</view>
				<view class="detail-right" style="margin-top: 4px;"> {{release_time}}</view>
				<view class="detail-right"> {{directors}}</view>
				<view class="detail-right"> {{writers}}</view>
				<view class="detail-right"> {{stars}}</view>
				<view class="detail-right" style=" width: calc(80%);"> {{intro}}</view>
			</view>
			<u-rate class="detail-right" style="margin-top: 420px; margin-left: 640px;" active-color="#ffea00" inactive-color="#b2b2b2" :value="3.7" size="30" readonly></u-rate>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				id : 0,
				movie_id: 0, 
				name: "",	//电影名称
				time: "",	//电影时长
				genre: "",			//电影类别
				release_time: "",	//发行时间
				intro: "",			//简介
				directors: "",		//导演
				writers: "",		//作者
				stars: "",			//明星
				pic_path: "",		// 图片
			}
		},
		onLoad(option) {
			this.id = option.id
			this.movie_id = option.movie_id
			uni.request({
				url: 'http://82.156.202.134:23333/api/mdetail/moviedetail?movie_id=' + this.movie_id,
				method: 'POST',
				success: res => {
					this.name = res.data.result.name.slice(0,-8)
					this.time = res.data.result.time
					this.genre = res.data.result.genre
					this.release_time = res.data.result.release_time
					this.intro = res.data.result.intro
					this.directors = res.data.result.directors
					this.writers = res.data.result.writers
					this.stars = res.data.result.starts
					this.pic_path = res.data.result.url
				},
			})
		},
		methods: {
			navi_main(){
				uni.navigateTo({
					url: "/pages/main?id=" + this.id,
				})
			},
		}
	}
</script>

<style>
	page{
		overflow-y: auto;
		background-color: #000000;
	}
	@font-face{
		font-family: cute;
		src: url('~@/static/NoganasRegular-mL73m.ttf');
		@include flex;
		flex-direction: row;
		flex-wrap: wrap;
		align-items: center;
	}
	@font-face{
		font-family: name;
		src: url('~@/static/Creatball-VGjpe.ttf');
		@include flex;
		flex-direction: row;
		flex-wrap: wrap;
		align-items: center;
	}
	@font-face{
		font-family: regular;
		src: url('~@/static/TrackwalkerDemo-1Gy7j.ttf');
		@include flex;
		flex-direction: row;
		flex-wrap: wrap;
		align-items: center;
	}
	@font-face{
		font-family: title;
		src: url('~@/static/PostersItalicPersonalUseBoldItalic-ALqx6.ttf');
		@include flex;
		flex-direction: row;
		flex-wrap: wrap;
		align-items: center;
	}
	.title{
		margin-top: 13px;
		margin-left: 10px;
		font-family: title;
		color: #ffffff;
		font-size: calc(60%);
	}
	.navi{
		height: 80px;
		z-index:5;
		position: fixed;
		width: calc(100%);
		/* box-shadow: 0px 3px 5px 0px rgba(0, 0, 0, 0.1); */
		background: linear-gradient(#00000055, #00000000 99%);
	}
	.portrait{
		margin-top: 10px;
	}
	.bg_img{
		height: calc(100%);
		width: calc(100%);
		position: fixed;
		-webkit-mask: radial-gradient(black 50%, transparent 100%);
	}
	.detail-box{
		margin-top: calc(5%);
		margin-bottom: calc(5%);
		position: absolute;
		width: calc(100%);
		height: 1500rpx;
		line-height: 2;
		
		overflow: hidden;
	}
	.detail-glass{
		width: calc(100%);
		height: 1100rpx;
		-webkit-mask: linear-gradient(#ffffff55,#000000, #000000, #000000, #000000, #ffffff55);
		-webkit-filter: blur(10px);
		   -moz-filter: blur(10px);
		    -ms-filter: blur(10px);    
		        filter: blur(10px); 
	}
	.detail-img{
		margin-top: calc(5%);
		margin-left: calc(10%);
		height: 800rpx;
		position: absolute;
		z-index:2;
		border-radius: 2%;
		border: 5rpx solid #ffffff;
	}
	.detail-info{
		position: fixed;
		margin-top: calc(5%);
		margin-left: calc(30%);
		background-color: #00000066;
		width: calc(60%);
		height: 800rpx;
	}
	.detail-title{
		margin-top: 0px;
		margin-left: calc(4%);
		font-family: name;
		font-size: 100rpx;
		color: #ffffff;
	}
	.detail-left{
		position: fixed;
		margin-left: calc(2%);
		font-size: 35rpx;
		font-family: regular;
		color: #ffffff;
	}
	.detail-right{
		margin-left: calc(20%);
		font-size: 35rpx;
		color: #ffffff;
	}
</style>
