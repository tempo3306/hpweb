			var lowestprice = 88000; //此时的最低成交价
			var realsecond = 0 //真实秒钟
			var viewsecond = 0 //显示秒钟
			var accept_second = 0 //最低成交价接受时间
			var price_limit = 10 //随机种子，影响跳价情况
			var time_torrent = 10 //随机种子，影响时间显示情况
			var price_torrent = 0

			var delay = 2 //随机动态延迟
			var no_image = 90 //随机出现验证码刷新失败，出现验证码的概率
			var userprice1 = 0 //用户出价
			var userprice2=0
			count=0  //出价次数
			var usertime1=0 //用户出价时间第一次
			var usertime2=0 //用户出价时间第二次
			var interval = 4 //4秒内不能查看验证码
			var query_time = 0 //最近一次查看验证码的时间
			var accept_time = 60 //接受时间
			var running = true //是否进行中
            var usercode=0 //用户验证码
            //日期获取
            var date=new Date();
            var year=date.getFullYear();
            var month=date.getMonth()+1;  //0-11
            var day=date.getDate();
            var today=year.toString()+'-'+month.toString()+'-'+day.toString();
            $(document).ready(function(){$('#li3').html("出价时间:"+today+" 10:30:5");});
			//创建记录数组
			var pt1 = [];
			var pt2 = [];
	
			var xp=window.screen.width;var yp=window.screen.height;
			$(document).ready(function(){$('body').css({"postion":"relative","left":xp/2-450,"top":0})});
			//获取主背景位置
			
			lowestprice = 88000 + parseInt((Math.random() - 0.5) * 40) * 100;
//-----------------------------------------------------------------------------------------------
//系统模块
//随机种子，影响跳价情况
            var x1=Math.random() < 0.5 ? 1 : (-1)   //随机+-
            price_torrent = parseInt((Math.random()) * 20)*x1; //20档跳价
			var price_limit1 = 10+price_torrent/4;  //0-40     10%之间概率跳价
			var price_limit2 = 35+price_torrent/2;  //40~50    35%之间概论跳价
			var price_limit3 = 50+price_torrent;  //50-60     50%概论跳价




//随机种子，影响接受时间,初始化的时候确定，时间每一秒的读秒时间由这个时间的百分比确定
			time_torrent = Math.random()/2+0.5 //随机种子，影响时间显示情况    0.5-1
			var time_cut = Math.random()*5+53 // 随机一个时间分隔因子   平均时间55.5
            var time_need1=time_torrent-0.5  //52秒之前
            var time_need2=time_torrent    //52到time_cut之间
            var time_need3=2      //time_cut之后  + time_torrent*n   n为当前时间与时间种子差值
//随机显示状态
            var view_torrent=Math.random()*10



//-----------------------------------------------------------------------------------------------
			//限制只能输入数字
			$(function() {
				$('input').keypress(function(e) {
					if(!String.fromCharCode(e.keyCode).match(/[0-9\.]/)) {
						return false;
					}
				})
			});
			function selectFromMess() {
    return arguments[Math.floor(Math.random() * arguments.length)]
}

//执行功能
			setInterval("Calculate_time()", 100);
			setInterval("Calculate_price()", 1000);
//模拟价格波动
			function Calculate_price() {
				var price_grow = Math.random()*100;
				if(running) {
					text1 = lowestprice.toString() + '元';
					$('.lowestprice').text(text1);
	            //根据时间随机跳价
					if(realsecond<40){
					if(price_grow <= price_limit1) {
						lowestprice = lowestprice + 100;
						pt1.push(lowestprice);-
						pt2.push(realsecond);
					}}
                    else if(realsecond>=40&&realsecond<50){
					if(price_grow <= price_limit2) {
						lowestprice = lowestprice + 100;
						pt1.push(lowestprice);
						pt2.push(realsecond);
					}
                    }
                    else{
					if(price_grow <= price_limit3) {
						lowestprice = lowestprice + 100;
						pt1.push(lowestprice);
						pt2.push(realsecond);
					}
                    }
					$(".leftprice").text(lowestprice);
					$(".pricerange").text((lowestprice - 300) + '至' + (lowestprice + 300));
				}
			};
//模拟时间
			function Calculate_time() {
				if(running) {
					realsecond = realsecond + 0.1;
					view=view_torrent+realsecond/5; //时间靠后越容易卡住时间
					if(realsecond < 59.9) {
						var randomview = parseInt(100 * Math.random());
						$('.systemtime').text("11:29:" + realsecond);
						if(randomview > view) {
							viewsecond = realsecond
						};
						viewsecond = parseInt(viewsecond)
						$('.systemtime').text("11:29:" + viewsecond);
						if(viewsecond >= 3) {
							$('.lasttime').text("11:29:" + (viewsecond - 3))
						} else {
							$('.lasttime').text("11:29:0")
						};

					} else {
						$('#final-info').dialog("open");
						running = false;
                        $('.userwriteprice').val('');
						setTimeout(result, 3000)
					};
//模拟结果判定
					function result() {
					if(userprice1>=userprice2){var userprice=userprice1;var usertime=usertime1}
					else{var userprice=userprice1;var usertime=usertime1};
						var index1 = pt1.indexOf(userprice);
						//判定最低成交价是否接受
						if(usertime<=60){
						if(userprice == lowestprice) {
							if(index1 !== -1) {
								var tem1 = usertime - pt2[index1];
								var tem2 = selectFromMess(0.5,1,1.5,2);
								if(tem1 > tem2) {
									$('#info-result-failure').dialog("open")
								}
							}
						}
						else if(userprice > lowestprice) {
							$('#info-result-success').dialog("open")
						}
						else
						{
							$('#info-result-failure').dialog("open")
						};
					}
					else{
					$('#outoftime').dialog("open")     //超过截止时间
					}
					}
				}
			};
//复位，重新开始
			function Reset() {
				running = true;
				count=0;
				realsecond = 0;
				viewsecond = 0;
				usertime1=0;
				usertime2=0;
				userprice1=0;
				userprice2=0;
				//随机创建随机数
				lowestprice = 87000 + parseInt((Math.random() - 0.35) * 40) * 100;
//系统模块
//随机种子，影响跳价情况
            var x1=Math.random() < 0.5 ? 1 : (-1)   //随机+-
            price_torrent = parseInt((Math.random()) * 20)*x1; //20档跳价
			var price_limit1 = 10+price_torrent/4;  //0-40     10%之间概率跳价
			var price_limit2 = 35+price_torrent/2;  //40~50    35%之间概论跳价
			var price_limit3 = 50+price_torrent;  //50-60     50%概论跳价
//随机种子，影响接受时间,初始化的时候确定，时间每一秒的读秒时间由这个时间的百分比确定
			time_torrent = Math.random()/2+0.5 //随机种子，影响时间显示情况    0.5-1
			var time_cut = Math.random()*5+53 // 随机一个时间分隔因子   平均时间55.5
            var time_need1=time_torrent-0.5  //52秒之前
            var time_need2=time_torrent    //52到time_cut之间
            var time_need3=2      //time_cut之后  + time_torrent*n   n为当前时间与时间种子差值
//随机显示状态
            var view_torrent=Math.random()*10
			}

//产生一个进度条，模拟读秒
			function ProgressOn(t) {
				$('#price-form').dialog("open");
				$("#progressbar").progressbar({
					value: 0
				});
				doProgressbar();
				var tem1 = 1/t;  //每秒百分比速度
                var width_now=0;
				function doProgressbar(t) {
					width_now = tem1 * 350+width_now;
					if(width_now>=350)width_now=350;
					$(".progressbar").width(width_now);
					if(width_now >= 350) {
						Read_price();
					};
					if(width_now>= 350) {
                        $('#price-form').dialog("close");
						$(".progressbar").width(0);
						return;
					};
					setTimeout(doProgressbar, 100);
				}
			}
//出价情况判定
			function Read_price() {
				usercode = $('.inputyanzhengma').val();
                var temp_price=$('.userwriteprice').val();
                $('#inputyanzhengma').val('');   //清空输入框
				if(usercode != answer) {
					$("#info-wrongcode").dialog("open");
				} else if((userprice > lowestprice + 300) || (userprice < lowestprice - 300)) {
					$('#price-wrong').dialog("open");
				} else if(usertime1 >= 59&&count==0) {
					$('#outoftime').dialog('open');
				} else if(usertime2 >= 59&&count==1) {
					$('#outoftime').dialog('open');
				} else {
				    if(count==0)
				    {userprice1=temp_price;usertime1 = realsecond;$('#price-right').dialog("open");count=1;
				    $('#li1').html("您第二次出价");
				    $('#li2').html("出价金额:"+userprice1);
				    $('#li3').html("出价时间:"+today+" 10:30:5"+parseInt(usertime1));
				    }
					else
					{userprice2=temp_price;usertime2=realsecond;$('#price-right').dialog("open");count=2;
									    $('#li1').html("您第三次出价");
				    $('#li2').html("出价金额:"+userprice2);
				    $('#li3').html("出价时间:2017-7-9 11:29:"+parseInt(usertime2));}
				}
			}

//判定是否刷出来验证码
			function No_image() {
				var random_no = 100 * Math.random();
				if(random_no > no_image) {
					return False
				} else {
					return True
				}
			}
			//判定是否可以查看验证码
			function Interval() {
				time1 = realsecond - query_time;
				if(time1 >= realsecond) {
					return true
				} else {
					return false
				}
			}
//判定价格正确
			function Price_confirm() {
				userprice = parseInt($('.userwriteprice').val());
				if(userprice % 100 == 0) {
					return true
				} else {
					return false
				}
			}
//判定验证码是否回答正确
			function Answer(useranswer) {
				if(useranswer == answer) {
					return true
				} else {
					return false
				}
			}

//绑定+-按纽功能
			$(document).ready(function() {
				$("#b1").click(function() {
					$(".userwriteprice").val(lowestprice - 300);
				})
			});
			$(document).ready(function() {
				$("#b2").click(function() {
					$(".userwriteprice").val(lowestprice - 200);
				})
			});
			$(document).ready(function() {
				$("#b3").click(function() {
					$(".userwriteprice").val(lowestprice - 100);
				})
			});
			$(document).ready(function() {
				$("#b4").click(function() {
					$(".userwriteprice").val(lowestprice + 300);
				})
			});
			$(document).ready(function() {
				$("#b5").click(function() {
					$(".userwriteprice").val(lowestprice + 200);
				})
			});
			$(document).ready(function() {
				$("#b6").click(function() {
					$(".userwriteprice").val(lowestprice + 100);
				})
			});
			//绑定加价按纽功能
			$(document).ready(function() {
				$("#jiajia").click(function() {
					var A = $('.useraddprice').val();
					if(A == "") {
						var useradd = lowestprice
					} else {
						var useradd = lowestprice + parseInt(A)
					};
					$(".userwriteprice").val(useradd);
				})
			});
//绑定出价按纽功能，弹出对话框
			$(function() {
//验证码框实现
				$("#dialog-form").dialog({
					open: function(event, ui) {
						closeOnEscape: false, //取消esc键 
						$(".ui-dialog-titlebar").hide();
					},
					draggable: false,
					resizable: false,
					autoOpen: false,
					height: 306,
					width: 439,
					modal: true,
					position: {
						using: function() {　　　　　　
							$(this).css({　　　　　　　　
								"position": "absolute",
								　　　　　　　　"top": "237px", //设置弹出框距离是页面顶端下的200px
								　　　　　　　　"left": "428px" //设置弹出框距离是页面顶端下的200px
								　　　　　　
							});　　　　
						}
					}
				});
//系统提示请求验证码过于频繁
				$("#info-quick").dialog({
					open: function(event, ui) {
						closeOnEscape: false, //取消esc键 
						$(".ui-dialog-titlebar").hide();
					},
					draggable: false,
					resizable: false,
					autoOpen: false,
					height: 306,
					width: 439,
					modal: true,
					position: {
						using: function() {　　　　　　
							$(this).css({　　　　　　　　
								"position": "absolute",
								　　　　　　　　"top": "237px", //设置弹出框距离是页面顶端下的200px
								　　　　　　　　"left": "428px" //设置弹出框距离是页面顶端下的200px
								　　　　　　
							});　　　　
						}
					}
				});
//系统提示出价过快
				$("#info-tooquick").dialog({
					open: function(event, ui) {
						closeOnEscape: false, //取消esc键 
						$(".ui-dialog-titlebar").hide();
					},
					draggable: false,
					resizable: false,
					autoOpen: false,
					height: 306,
					width: 439,
					modal: true,
					position: {
						using: function() {　　　　　　
							$(this).css({　　　　　　　　
								"position": "absolute",
								　　　　　　　　"top": "237px", //设置弹出框距离是页面顶端下的200px
								　　　　　　　　"left": "428px" //设置弹出框距离是页面顶端下的200px
								　　　　　　
							});　　　　
						}
					}
				});
//系统提示验证证码错误
				$("#info-wrongcode").dialog({
					open: function(event, ui) {
						closeOnEscape: false, //取消esc键 
						$(".ui-dialog-titlebar").hide();
					},
					draggable: false,
					resizable: false,
					autoOpen: false,
					height: 306,
					width: 439,
					modal: true,
					position: {
						using: function() {　　　　　　
							$(this).css({　　　　　　　　
								"position": "absolute",
								"top": "237px", //设置弹出框距离是页面顶端下的200px
								"left": "428px" //设置弹出框距离是页面顶端下的200px
							});　　　　
						}
					}
				});
//系统提示价格错误
				$("#info-wrongprice").dialog({
					open: function(event, ui) {
						closeOnEscape: false, //取消esc键 
						$(".ui-dialog-titlebar").hide();
					},
					draggable: false,
					resizable: false,
					autoOpen: false,
					height: 306,
					width: 439,
					modal: true,
					position: {
						using: function() {　　　　　　
							$(this).css({　　　　　　　　
								"position": "absolute",
								　　　　　　　　"top": "237px", //设置弹出框距离是页面顶端下的200px
								　　　　　　　　"left": "428px" //设置弹出框距离是页面顶端下的200px
							});　　　　
						}
					}
				});
//出价有效
				$("#price-right").dialog({
					open: function(event, ui) {
						closeOnEscape: false, //取消esc键 
						$(".ui-dialog-titlebar").hide();
					},
					draggable: false,
					resizable: false,
					autoOpen: false,
					height: 306,
					width: 439,
					modal: true,
					position: {
						using: function() {　　　　　　
							$(this).css({　　　　　　　　
								"position": "absolute",
								　　　　　　　　"top": "237px", //设置弹出框距离是页面顶端下的200px
								　　　　　　　　"left": "428px" //设置弹出框距离是页面顶端下的200px
							});　　　　
						}
					}
				});
//系统提示价格不在区间
				$("#price-wrong").dialog({
					open: function(event, ui) {
						closeOnEscape: false, //取消esc键 
						$(".ui-dialog-titlebar").hide();
					},
					draggable: false,
					resizable: false,
					autoOpen: false,
					height: 306,
					width: 439,
					modal: true,
					position: {
						using: function() {　　　　　　
							$(this).css({　　　　　　　　
								"position": "absolute",
								　　　　　　　　"top": "237px", //设置弹出框距离是页面顶端下的200px
								　　　　　　　　"left": "428px" //设置弹出框距离是页面顶端下的200px
							});　　　　
						}
					}
				});
//系统提示超时
				$("#outoftime").dialog({
					open: function(event, ui) {
						closeOnEscape: false, //取消esc键 
						$(".ui-dialog-titlebar").hide();
					},
					draggable: false,
					resizable: false,
					autoOpen: false,
					height: 306,
					width: 439,
					modal: true,
					position: {
						using: function() {　　　　　　
							$(this).css({　　　　　　　　
								"position": "absolute",
								　　　　　　　　"top": "237px", //设置弹出框距离是页面顶端下的200px
								　　　　　　　　"left": "428px" //设置弹出框距离是页面顶端下的200px
							});　　　　
						}
					}
				});
//系统提示结果失败
				$("#info-result-failure").dialog({
					open: function(event, ui) {
						closeOnEscape: false, //取消esc键 
						$(".ui-dialog-titlebar").hide();
					},
					draggable: false,
					resizable: false,
					autoOpen: false,
					height: 306,
					width: 439,
					modal: true,
					position: {
						using: function() {　　　　　　
							$(this).css({　　　　　　　　
								"position": "absolute",
								　　　　　　　　"top": "237px", //设置弹出框距离是页面顶端下的200px
								　　　　　　　　"left": "428px" //设置弹出框距离是页面顶端下的200px
								　　　　　　
							});　　　　
						}
					}
				});
//系统提示结果成功

				$("#info-result-success").dialog({
					open: function(event, ui) {
						closeOnEscape: false, //取消esc键 
						$(".ui-dialog-titlebar").hide();
					},
					draggable: false,
					resizable: false,
					autoOpen: false,
					height: 306,
					width: 439,
					modal: true,
					position: {
						using: function() {　　　　　
							$(this).css({　　　　　　　
								"position": "absolute",
								　　　　　　　　"top": "237px", //设置弹出框距离是页面顶端下的200px
								　　　　　　　　"left": "428px" //设置弹出框距离是页面顶端下的200px
							});　　　　
						}
					}
				});
//时间到界面跳转
				$("#final-info").dialog({
					open: function(event, ui) {
						closeOnEscape: false, //取消esc键 
						$(".ui-dialog-titlebar").hide();
					},
					draggable: false,
					resizable: false,
					autoOpen: false,
					height: 476,
					width: 379,
					modal: true,
//					position:{  				
//						my: "left top",
//						at: "left top+169 ",
//						of: $('.leftmainbox')}
					position: {
						using: function() {　　　　　　
							$(this).css({　　　　　　　　
								"position": "absolute",
								"top": "169px",
								"left": "22px",
//								"top": (yp/2-215).toString(),
//								"left": (xp/2-428).toString()
							});　　　　
						}
					}
				});
//				var $div = $('.leftmainbox');
//				$("#final-info").dialog('widget').position({
//				my: "center",
//				at: "left-400 top ",
//				of: $div
//				});
				
				
				$(".middleconfirm").button().click(function() {
					$("#info-form").dialog("close");
				});
				$(".middleconfirm_wrongcode").button().click(function() {
					$("#info-wrongcode").dialog("close");
					$("#dialog-form").dialog("close");
				});
				$(".middleconfirm_wrongprice").button().click(function() {
					$("#info-wrongcode").dialog("close");
				});
				$(".middleconfirm_result").button().click(function() {
					$("#info-form").dialog("close");
				});
//出价处理
				$("#price-form").dialog({
					open: function(event, ui) {
						closeOnEscape: false, //取消esc键 
						$(".ui-dialog-titlebar").hide();
					},
					draggable: false,
					resizable: false,
					autoOpen: false,
					height: 306,
					width: 439,
					modal: true,
					position: {
						using: function() {　　　　　　
							$(this).css({　　　　　　　　
								"position": "absolute",
								　　　　　　　　"top": "237px", //设置弹出框距离是页面顶端下的200px
								　　　　　　　　"left": "428px" //设置弹出框距离是页面顶端下的200px
								　　　　　　
							});　　　　
						}
					}
				});

				$("#chujia").button().click(function() {
					var price100 = Price_confirm();
					var interval1 = Interval();
					if(price100 && interval1) {
					var id=Math.floor(Math.random()*100+1);
					var path_yanzhengma="/yanzhengma/"+id;
					var path_answer="/answer/"+id;

					$.get(path_answer,null,function(ret){question=ret.question;answer=ret.answer;});  //获取答案和问题
					$('#question').text(question);

 					    $("#yanzhengma").load(path_yanzhengma);//加载验证码
						$("#dialog-form").dialog("open");
					} else if(!(interval1)) {
						$("#info-tooquick").dialog("open")
					} else if(!(price100)) {
						$("#info-wrongprice").dialog("open")
					};

				});
				$(".middleconfirm_wrongcode").button().click(function() {
					$("#info-wrongcode").dialog("close");
				});
				$(".middleconfirm_wrongprice").button().click(function() {
					$("#info-wrongprice").dialog("close");
				});
				$(".cancel").button().click(function() {
					$("#dialog-form").dialog("close");
				});
				$(".confirm").button().click(function() {
					var t = 0;
					if(realsecond < 52) {
						t = time_need1
					}
					else if(realsecond > 52 && realsecond <=time_cut) {
						t = time_need2
					}
					 else {
						t = time_torrent*(realsecond-time_cut)+2
					}

					ProgressOn(t);
				});

				$(".middleconfirm_priceright").button().click(function() {
					$("#price-right").dialog("close");
					$("#dialog-form").dialog("close");
				});


				$(".middleconfirm_outoftime").button().click(function() {
					$("#dialog-form").dialog("close");
					$("#outoftime").dialog("close");
				});
				$(".middleconfirm_pricewrong").button().click(function() {
					$("#price-wrong").dialog("close");
					$("#dialog-form").dialog("close");
				});
				$(".middleconfirmsuccess").button().click(function() {
//					history.go(0);
$('#final-info').dialog("close");
$('#info-result-success').dialog("close");
Reset();
				});
				$(".middleconfirmfailure").button().click(function() {
					$('#final-info').dialog("close");
$('#info-result-failure').dialog("close");
Reset();
				});

			});