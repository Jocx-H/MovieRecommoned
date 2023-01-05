<!--
@File   : main.vue
@Time   : 2023/1/1 ‏‎16:11:23
@Author : Sparkling-Y
@Desc   : 主页
-->

<template>
	<view>
		<!-- 顶部导航栏 -->
		<view class="navi">
			<uni-row>
				<!-- title -->
				<uni-col :span="22">
					<view class="title">
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
		<!-- 主要内容 -->
		<view>
			<image class="bg_img" src="../static/bg.jpg" mode="aspectFill"></image>
			<!-- 侧边分类导航栏 -->
			<scroll-view  class="genre" scroll-y="true"@scrolltoupper="upper" @scrolltolower="lower" @scroll="scroll">
				<view class="btn" :style="{'color': (genre_index==0 ? '#999999':'#424242')}" @click="change_genre(0)">Recommend</view>
				<view class="btn" :style="{'color': (genre_index==1 ? '#999999':'#424242')}" @click="change_genre(1)">Action</view>
				<view class="btn" :style="{'color': (genre_index==2 ? '#999999':'#424242')}" @click="change_genre(2)">Adventure</view>
				<view class="btn" :style="{'color': (genre_index==3 ? '#999999':'#424242')}" @click="change_genre(3)">Animation</view>
				<!-- <view class="btn" :style="{'color': (genre_index==4 ? '#999999':'#424242')}" @click="change_genre(4)">Children</view> -->
				<view class="btn" :style="{'color': (genre_index==5 ? '#999999':'#424242')}" @click="change_genre(5)">Comedy</view>
				<view class="btn" :style="{'color': (genre_index==6 ? '#999999':'#424242')}" @click="change_genre(6)">Fantasy</view>
				<!-- <view class="btn" :style="{'color': (genre_index==7 ? '#999999':'#424242')}" @click="change_genre(7)">IMAX</view> -->
				<view class="btn" :style="{'color': (genre_index==8 ? '#999999':'#424242')}" @click="change_genre(8)">Romance</view>
				<view class="btn" :style="{'color': (genre_index==9 ? '#999999':'#424242')}" @click="change_genre(9)">Sci-Fi</view>
				<view class="btn" :style="{'color': (genre_index==10 ? '#999999':'#424242')}" @click="change_genre(10)">Western</view>
				<view class="btn" :style="{'color': (genre_index==11 ? '#999999':'#424242')}" @click="change_genre(11)">Crime</view>
				<view class="btn" :style="{'color': (genre_index==12 ? '#999999':'#424242')}" @click="change_genre(12)">Mystery</view>
				<view class="btn" :style="{'color': (genre_index==13 ? '#999999':'#424242')}" @click="change_genre(13)">Drama</view>
				<view class="btn" :style="{'color': (genre_index==14 ? '#999999':'#424242')}" @click="change_genre(14)">Thriller</view>
				<view class="btn" :style="{'color': (genre_index==15 ? '#999999':'#424242')}" @click="change_genre(15)">War</view>
				<view class="btn" :style="{'color': (genre_index==16 ? '#999999':'#424242')}" @click="change_genre(16)">Horror</view>
				<view class="btn" :style="{'color': (genre_index==17 ? '#999999':'#424242')}" @click="change_genre(17)">Film-Noir</view>
				<view class="btn" :style="{'color': (genre_index==18 ? '#999999':'#424242')}" @click="change_genre(18)">Documentary</view>
				<view class="btn" :style="{'color': (genre_index==19 ? '#999999':'#424242')}" @click="change_genre(19)">Musical</view>
				<!-- <view class="btn" :style="{'color': (genre_index==20 ? '#999999':'#424242')}" @click="change_genre(20)">Others</view> -->
			</scroll-view>
			<!-- 推荐电影 -->
			<view class="recommend">
				<view class="recommend_box">
					<uni-row>
						<uni-col :span="4" v-for="(item, i) in temp_5" :key="i+'b'">
							<view class="rec_movie">
								<image class="movie_img" :src="movie_pic[item]" mode="scaleToFill" @click="toDetail(item)">
								</image>
							</view>
							<text class="rec_movie_name"> {{movie_name[item]}} </text>
						</uni-col>
					</uni-row>
					<uni-row>
						<uni-col :span="4" v-for="(item, i) in temp_10" :key="i+'b'">
							<view class="rec_movie">
								<image class="movie_img" :src="movie_pic[item]" mode="scaleToFill" @click="toDetail(item)"
								></image>
							</view>
							<text class="rec_movie_name"> {{movie_name[item]}} </text>
						</uni-col>
					</uni-row>
				</view>
			</view>
			<!-- 选择页数 -->
			<view class="page_picker" v-if="genre_index!=0">
				<uni-row>
					<uni-col :span="1" :offset="6">
						<u-icon name="arrow-leftward" size="30" style="cursor: pointer;" @click="last()"></u-icon>
					</uni-col>
					<uni-col :span="3" style="margin-top: 3px;cursor: pointer;" :style="{'color': (color_left ? '#ffffff':'#828282')}" @click="last()">
						<view @click="last()">last page</view>
					</uni-col>
					<uni-col :span="2" style="margin-top: 3px;cursor: pointer;" :style="{'color': (color_right ? '#ffffff':'#828282')}" @click="next()">
						<view @click="next()">next page</view>
					</uni-col>
					<uni-col :span="1">
						<u-icon name="arrow-rightward" size="30" style="cursor: pointer;" @click="next()"></u-icon>
					</uni-col>
				</uni-row>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				id: 0,
				temp_5: [0,1,2,3,4,5],
				temp_10: [6,7,8,9,10,11],
				colors: ['#ffffff','#828282'],
				color_left: false,
				color_right:false,
				genre_index: 0,	// 选择的类别
				movie_id:[],
				movie_pic: [],	// 电影封面图片地址
				movie_name: [],	// 电影名称
				page:1,
			}
		},
		methods: {
			change_genre(i){
				this.page = 1
				this.genre_index = i
				console.log("genre_index:", this.genre_index)
				if (this.genre_index != 0){
					uni.request({
						url: 'http://82.156.202.134:23333/api/mfront/movielist?tag=' + this.genre_index + '&page_count=' + this.page,
						method: 'POST',
						success: res => {
							this.movie_id = res.data.result.id
							this.movie_name = res.data.result.name
							this.movie_pic = res.data.result.url
						},
					})
				}else{
					
				}

			},
			toDetail(i){
				uni.navigateTo({
					url: "/pages/detail?id=" + this.id + "&movie_id=" + this.movie_id[i],
				})
			},
			last(){
				if (this.page > 1){
					this.page = this.page - 1
					this.color_left = true
					setTimeout(() => {
					    this.color_left = false;
					}, 100);
					uni.request({
						url: 'http://82.156.202.134:23333/api/mfront/movielist?tag=' + this.genre_index + '&page_count=' + this.page,
						method: 'POST',
						success: res => {
							this.movie_id = res.data.result.id
							this.movie_name = res.data.result.name
							this.movie_pic = res.data.result.url
						},
					})
				}
			},
			next(){
				this.page = this.page + 1
				this.color_right = true
				setTimeout(() => {
				    this.color_right = false;
				}, 100);
				uni.request({
					url: 'http://82.156.202.134:23333/api/mfront/movielist?tag=' + this.genre_index + '&page_count=' + this.page,
					method: 'POST',
					success: res => {
						this.movie_id = res.data.result.id
						this.movie_name = res.data.result.name
						this.movie_pic = res.data.result.url
					},
				})
			}
		},
		onLoad(option){
			this.id = option.id
			uni.request({
				url: 'http://82.156.202.134:23333/api/recom/hotmovie',
				method: 'GET',
				success: res => {
					this.movie_id = res.data.result.id
					this.movie_name = res.data.result.name
					this.movie_pic = res.data.result.url
				},
			})
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
	.genre{
		margin-top: calc(5%);
		background-color: #00000000;
		width: calc(15%);
		height: calc(88%);
		position: fixed;
		z-index: 4;
		font-size: 20rpx;
		font-family: cute;
		color: #ffffff;
	}
	.btn{
		font-family: cute;
		font-size: 40rpx;
		margin-bottom: 13rpx;
		margin-left: 40rpx;
		color: #838383;
		cursor: pointer;
		width: calc(40%);
	}
	.recommend{
		background: linear-gradient(#00000000, #000000 99%);
		width: calc(100%);
		height: calc(100%);
		position: fixed;
		font-size: 20rpx;
		z-index: 3;
		font-family: cute;
		color: #ffffff;
	}
	.recommend_box{
		margin-left: calc(10%);
		margin-top: calc(4%);
		margin-right: calc(5%);
		z-index: 6;
	}
	.bg_img{
		height: calc(100%);
		width: calc(100%);
		position: fixed;
		-webkit-mask: radial-gradient(black 50%, transparent 100%);
	}
	.rec_movie{
		z-index: 6;
		cursor:pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-left: 38px;
		margin-top: 18px;

	}
	.rec_movie_name{
		margin-top: 10px;
		margin-left: 35px;
		font-size: calc(80%);
		text-align: center;
		cursor:pointer;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.movie_img{
		border-top-left-radius: 10px; 
		border-top-right-radius: 10px;
		border-bottom-left-radius: 10px; 
		border-bottom-right-radius: 10px;
		-webkit-mask: radial-gradient(black 80%, transparent 100%);
	}
	.page_picker{
		margin-left: calc(15%);
		width: calc(100%);
		color: #ffffff;
		font-family: cute;
		font-size: 20px;
		position: fixed;
		margin-top: calc(44%);
		z-index: 10;
	}
	image{
		list-style: none;
		transition: .3s linear;
	}
	image:hover{
		transform: scale(1.01);
		-webkit-mask: radial-gradient(black 90%, transparent 100%);
	}
	image::before, image::after{
	    position: absolute;
	    content: '';
	    transition: 1.3s ease-out ;
	}
</style>
