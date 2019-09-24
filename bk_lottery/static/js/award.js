$(function() {
    // var setAwardBoxWidth = function() {
    //     var $box = $('.award-container .award-box');
    //     var height = $box.height();
    //     $box.css('width', height + 'px');
    // };
    // setAwardBoxWidth();

    var background = document.getElementById('background');
    var canvas = document.getElementById('space');
    canvas.width = $(window).width();
    canvas.height = $(window).height();
    var context = canvas.getContext('2d');
    context.drawImage(background, 0, 0, windowWidth, windowHeight);
    context.textAlign = "center";
    context.fillStyle = "white";

    var windowWidth = canvas.width;
    var windowHeight = canvas.height;
    var avatarShowPercent = 0.4;
    var avatarFocalLength = 10;
    var winnerFocalLength = 7;
    var sizeFactor = 100;
    if (windowWidth > 2000) {
        sizeFactor = 200;
        winnerFocalLength = 8;
    }
    var speed = 1.5;
    var winnerTick = 11; // 抽中中奖者时，中奖者将在n个tick后到达
    // var winnerSize = 400;
    var zRange = 400;
    var globalAlpha = 0.6;
    var clickInterval = 1000;
    if (award_number > 5) {
        clickInterval = 200;
        winnerTick = 6;
        winnerFocalLength = 2;
    }
    var max_avatar_n = Math.min(1000, rtxs.length);      // 动画显示头像的最大个数

    var isStopButtonActive = true;
    var isStopButtonShow = true;
    var isPausing = false;
    var intervalId;
    var allIntervalId;
    var shockIntervalId;

    var avatars = [];
    var winners = [];
    var fontSizes = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20,
        22, 24, 26, 28, 30, 32, 34, 36, 38, 40];

    var Avatar = function(name, url, x, y, z, focalLength) {
        this.image = document.createElement('img');
        this.image.src = url;
        this.name = name;
        this.x = x || (Math.random() * windowWidth - windowWidth / 2);
        this.y = y || (Math.random() * windowHeight - windowHeight / 2);
        this.z = z || (Math.random() * zRange - zRange / 2);
        this.focalLength = focalLength || avatarFocalLength || (Math.random() * 10 + 5)
        this.isWinner = false;
        this.display = Math.random() > avatarShowPercent ? false : true;
        this.showName = '';
        this.tick;

        this.render = function() {
            var scale = this.focalLength / (this.focalLength + this.z);
            var size = Math.max(1, Math.floor(scale * sizeFactor));
            var halfSize = size / 2;
            var x2d = (this.x * scale) + windowWidth / 2;
            var y2d = (this.y * scale) + windowHeight / 2;
            if (this.isWinner) {
                var lastAlpha = context.globalAlpha;
                context.globalAlpha = 1.0;
                context.drawImage(this.image, x2d - halfSize, y2d - halfSize, size, size);
                this.drawNameBySize(size, x2d, y2d);
                this.tick -= 1;
                if (this.tick == 0) {
                    clearInterval(intervalId);
                    this.isWinner = false;
                    isStopButtonShow = false;
                    context.globalAlpha = 0;

                    if (allIntervalId != undefined) {
                        if (winners.length === award_number) {
                            allIntervalId = setTimeout(function() {
                                $('#comfirmButton').trigger('click');
                            }, clickInterval);
                        } else {
                            allIntervalId = setTimeout(function() {
                                $('#nextButton').trigger('click');
                            }, clickInterval);
                        }
                    }
                } else {
                    context.globalAlpha = lastAlpha - globalAlpha / winnerTick;
                    if (context.globalAlpha < 0 || context.globalAlpha > globalAlpha) {
                        context.globalAlpha = 0;
                    }
                }
            } else {

                context.drawImage(this.image, x2d - halfSize, y2d - halfSize, size, size);
            }
            this.nextTick();
        };

        this.nextTick = function() {
            this.z -= speed;
            if (this.z < -this.focalLength) {
                this.z += zRange;
                this.x = Math.random() * windowWidth - windowWidth / 2;
                this.y = Math.random() * windowHeight - windowHeight / 2;
                this.display = Math.random() > avatarShowPercent ? false : true;
            }
        };

        this.drawNameBySize = function(size, x2d, y2d) {
            var fontSize = 1;
            context.font = fontSize + 'px 微软雅黑';
            var measure = context.measureText(this.showName);
            while (size - measure.width > 1) {
                fontSize += 0.5;
                context.font = fontSize+ 'px 微软雅黑';
                measure = context.measureText(this.showName);
            }
            context.fillText(this.showName, x2d, y2d + size / 2 + fontSize);
        };
    };

    var initAvatar = function() {
//        for (var i = 0; i < rtxs.length; i++) {
        for (var i = 0; i < max_avatar_n; i++) {
            avatars.push(new Avatar(rtxs[i].name, rtxs[i].avatar));
        }
        avatars.sort(function(a, b) {
            return b.z - a.z;
        });
    };

    var renderAll = function() {
        context.save();
        context.globalAlpha = 1.0;
        context.drawImage(background, 0, 0, windowWidth, windowHeight);
        context.restore();
        for (var i = 0; i < avatars.length; i++) {
            if (avatars[i].display) {
                avatars[i].render();
            } else {
                avatars[i].nextTick();
            }
        }
    };

    var start = function() {
        if (isStopButtonActive) {
            context.globalAlpha = globalAlpha;
        }
        renderAll();
        return setInterval(function() {
            renderAll();
        }, 50);
    };


    var showWinners = function(winners) {
        if (winners.length == 0) return; // 中奖人员已经展示过了

        var interval = 0;
        if (winners.length != award_number){
            //修改了中奖者人数，添加删除dom元素
            var winner_box = $('.winners-boxs').children().first();
            if (winners.length > award_number) {
                for(var i=0; i<winners.length-award_number; i++){
                    winner_box.after(winner_box.clone(true));
                }
            }else {
                for(var i=0; i<award_number-winners.length; i++){
                    winner_box.siblings().first().remove();
                }
            }
            award_number = winners.length;
        }
        $('.winner-box').each(function(index) {
            var winner = winners.shift(0);
            if (winner != undefined) {
                for(var i=0; i<rtxs.length; i++){
                    if(winner.name == rtxs[i]['name']){
                        avatar_path = rtxs[i]['avatar']
                        // 头像如果不是默认的，则使用500头像
                        if (/default/.test(avatar_path)){
                            $(this).find('img.avatar').first().attr('src', avatar_path);
                        }else{
                            img_highreso_path = ceph_static_url + `avatars/${rtxs[i]['name']}.png`
                            $(this).find('img.avatar').first().attr('src', img_highreso_path);
                        }
                    }
                }
                $(this).find('.rtx-name').html(winner.name);
                $(this).find('.rtx-chinese-name').html(winner.chineseName);
                var thisDom = $(this);
                setTimeout(function() {
                    thisDom.css('opacity', '1');
                }, interval);
                interval += 0;
            }
        });
    };

    var hideWinners = function() {
        $('.winner-box').each(function(index) {
            $(this).css('opacity', '0');
        });
    };

    var adjustWidthFowWinner = function() {
        var width = parseInt($('.winners-boxs').css('width'));
        var maxRowCount = windowWidth > 4000 ? 16 : 6;
        var minRowCount = windowWidth > 4000 ? 6 : 3;
//        if (award_number > 50) {
//            maxRowCount = 32;
//        }
        var eachWidth, eachHeight, rows;
        
        if (award_number < minRowCount) {
            eachWidth = Math.floor(width / minRowCount)
        } else if (award_number <= maxRowCount) {
            eachWidth = Math.floor(width / award_number);
        } else {
            eachWidth = Math.floor(width / maxRowCount);
        }
        eachWidth = eachWidth - 30;
        $('.winners-boxs').css('font-size', (eachWidth / 25 + 5) + 'px');
        $('.winners-boxs').find('.winner-box, img.profile_bg').each(function(index, value) {
            $(value).css('width', eachWidth + 'px');
        });
        eachHeight = parseInt($('.winners-boxs').find('.winner-box').first().css('height'));
        rows = Math.floor((award_number + maxRowCount - 1) / maxRowCount);
//        $('.winners-boxs').css('height', eachHeight * rows + rows * 20);
    };

    var getWinnerFromServer = function() {
        if (!isStopButtonActive) {
            return;
        }
        isStopButtonActive = false;
        $.post(site_url + 'lottery/award/' + award_id + '/winner/', function(data) {
            if (data['result']) {
                for (var i = 0; i < avatars.length; i++) {
                    if (avatars[i].name === data['rtx'].name) {
                        winners.push(data['rtx']);
                        avatars[i].isWinner = true;
                        avatars[i].x = 0;
                        avatars[i].y = 0;
                        avatars[i].z = winnerFocalLength;
                        avatars[i].tick = winnerTick;
                        avatars[i].showName = data['rtx'].name + ' (' + data['rtx'].chineseName + ')';
                        avatars[i].display = true;
                        break;
                    }
                }
            } else {
                toastr.info(data['message']);
            }
        }, 'json');
    };

    // 去掉输入框、style奖品title
    var stylePrize = function(){
        var input = $("#award-input");
        var prize = escapeHtml(input.val());
        input.after(`<p>${prize}</p>`)
        input.remove();

        $("#prize_bg p, #prize_bg").addClass("drew");
        $("#prize_bg p").removeClass("init");
        $("#prize_bg").removeClass("input");
    }

    function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }

    var getAllWinnersFromServer = function() {
        if (!isStopButtonActive) {
            // 重抽逻辑，只更新重抽的中奖者
            $.ajax({
                url: site_url + 'lottery/redraw/',
                data: {award_id: award_id, winner_staff: absent_winner},
                dataType: 'json',
                type: 'POST',
                success: function(data){
                    if (data.result){
                        new_winner_staff = data.data.winner.name;
                    avatar_path = data.data.winner.avatar;

                    if (/default/.test(avatar_path)){
                            $redraw_icon.prev().attr('src', avatar_path);
                        }else{
                            img_highreso_path = ceph_static_url + `avatars/${new_winner_staff}.png`
                            $redraw_icon.prev().attr('src', img_highreso_path);
                        }
                    $redraw_icon.parent().siblings(".rtx-name").html(new_winner_staff)
                    $redraw_icon.parent().siblings(".rtx-chinese-name").html(data.data.winner.chineseName)

                    $('#comfirmButton').trigger('click');
                    stylePrize();
                    $("#background-img").attr("src", ceph_static_url + 'images/animation_bg.jpg')

                    }
                    else{
                        toastr.info(data.message);
                    }
                     },
                error: function(){
                    console.log('redraw request failed');
                }
            })

            return;
        }

        $.post(site_url + 'lottery/award/' + award_id + '/winners/', function(data) {
            if (data['result']) {
                for (var i = 0; i < rtxs.length; i++) {
                    var winner = data['winners'].find(function(element) {
                        return rtxs[i].name === element.name;
                    });
                    if (winner != undefined) {
                        winners.push(winner);
                    }
                }
                award_times -= 1;
                if (award_times > 0) {
                    isStopButtonActive = true;
                }
                setTimeout(function() {
                    $('#comfirmButton').trigger('click');
                }, 0);

                isStopButtonActive = false;
                stylePrize();
                $("#background-img").attr("src", ceph_static_url + 'images/animation_bg.jpg')
            } else {
                toastr.info(data['message']);
            }
        }, 'json').fail(function(data){
            toastr.error(JSON.parse(data.responseText)['message'])
        });

        // 关闭opener抽奖按钮
        // if (window.opener){
        //     window.opener.disableBtn(award_id);
        // }
    }

    var awardFadeOut = function() {
        $('.award-box').addClass('award-fadeOut');
//        $('.modal-button').css('opacity', '0.8');
    };

    var shockImage = function(image, x, y, size) {
        var xs = [0, 0, -2, 2, 0, 0, -2, 2];
        var ys = [2, -2, 0, 0, 2, -2, 0, 0];
        shockIntervalId = setInterval(function() {
            var offsetx = xs.shift();
            var offsety = ys.shift();
            if (offsetx === undefined) {
                clearInterval(shockIntervalId);
            } else {
                var lastAlpha = context.globalAlpha;
                context.globalAlpha = 1.0;
                context.drawImage(image, offsetx + x, offsety + y, size, size);
                context.globalAlpha = lastAlpha;
            }
        }, 50);
    };

    // $('.award-box').on('click', function() {
    //     if (award_times > 0) {
    //         $('#lotteryModal').modal('show');
    //     }
    // });

    $('#play-button').on('click', function() {
        if (award_times > 0) {
            $('#lotteryModal').modal('show');
        }
    });

    // 暂停按钮和继续按钮
    $('#pauseButton').on('click', function() {
        clearInterval(intervalId);
        isPausing = true;
        $('#pauseButton').hide();
        $('#continueButton').show();
    });

    $('#continueButton').on('click', function() {
        if (isStopButtonShow && isPausing) {
            intervalId = start();
            isPausing = false;
            $('#continueButton').hide();
            $('#pauseButton').show();
        }
    });
    $('#continueButton').hide();
    $('#draw-again').hide();

    $('#stopButton').on('click', function() {
        getWinnerFromServer();
        // $('#stopButton').hide();
        // $('#nextButton').show();
    });

    $('#nextButton').on('click', function() {
        if (!isStopButtonShow && !isStopButtonActive && winners.length < award_number) {
            isStopButtonShow = true;
            isStopButtonActive = true;
            intervalId = start();

            if (allIntervalId == undefined) {
                $('#nextButton').hide();
                $('#stopButton').show();
            }
        }

        if (allIntervalId != undefined) {
            allIntervalId = setTimeout(function() {
                $('#stopButton').trigger('click');
            }, 500);
        }
    });
    $('#nextButton').hide();

    $('#allButton').on('click', function() {
        if (allIntervalId == undefined) {
            allIntervalId = setTimeout(function() {
                $('#stopButton').trigger('click');
            }, 0);
        }
    });

    $('#multiWinnersButton').on('click', function() {
        getAllWinnersFromServer();
    });

    $('#comfirmButton').on('click', function() {
        if (!isChangeNumber && winners.length !== award_number)
        {
//            console.log('请打开更改人数开关');
            console.log(`winners length: ${winners.length}, award_number: ${award_number}`)
        }else{
            $('.award-box').addClass('awarded');
            showWinners(winners);
            $('.winners-boxs').show();
            adjustWidthFowWinner();

            var winner_boxs = $('.winners-boxs').get(0)
            if (winner_boxs.clientHeight < winner_boxs.scrollHeight && award_number > 12){

                scrollSpeed = winner_boxs.scrollHeight/30000;
                var marginDiv = $("<div class='margin'></div>");
                marginDiv.height(winner_boxs.clientHeight);
                var $box1 = $('.winners-boxs');
                $box1.append(marginDiv.clone());
                $box1.prepend(marginDiv.clone());

                $box1[0].scrollTop = $box1.height();

                var offsetToScroll = $box1[0].scrollHeight - $box1.height()*2;
                var offsetToReset = $box1[0].scrollHeight - $box1.height();

                var $box2;
                var box1Ready = false;
                var loop = function(){
                    if (!$box2){
                        $box2 = $box1.clone();
                        $box2.insertAfter($box1);
                        $box2.css("top", -$box1.height())
                    }
                    $box2[0].scrollTop = 0;
                    box1Ready = false;

                    $box2.animate({scrollTop:offsetToScroll}, (offsetToScroll-$box2.scrollTop())/scrollSpeed,
                    "linear", function(){
                        $box2.animate({scrollTop: offsetToReset}, (offsetToReset-$box2.scrollTop())/scrollSpeed, "linear", function(){
                            $box2.scrollTop(0);
                        })

                        $box1.scrollTop(0);
                        $box1.animate({scrollTop: offsetToScroll}, offsetToScroll/scrollSpeed, "linear", loop);
                    });

                    $box1.animate({scrollTop:offsetToReset}, (offsetToReset-$box1[0].scrollTop)/scrollSpeed,
                     "linear",
                     function(){$box1.scrollTop(0);})
                }

                $box1.animate({scrollTop:offsetToScroll}, (offsetToScroll-$box1[0].scrollTop)/scrollSpeed,
                 "linear"
                 , loop)
            }
        }
        $('.awarded-number').html(winners.length);
        $('#lotteryModal').modal('hide');
        if (need_input) {
            $('#draw-again').fadeIn("slow");
        }
    });

    // 再抽一次
    $("#draw-again").on('click', function(){
        $.ajax({
            url: site_url + 'lottery/award/more/',
            data: {award_id: award_id},
            dataType: "html",
            success: function(html){
                $("body").html(html);
            }
        })
    })

    function randomSort(a, b) {
        return Math.random() > 0.5 ? -1 : 1;
    }

    var $redraw_icon;
    var absent_winner;
    $(".redraw").on('click', function(event){
        absent_winner = $(event.currentTarget.parentElement).next().text();
        $redraw_icon = $(event.currentTarget);
        $('#lotteryModal').modal('show');
    })

    $('#lotteryModal').on('hide.bs.modal', function() {
        clearInterval(intervalId);
        $('.operate-button').hide();
        if (award_times > 0)
            $('#play-button').show();
        else
            $('#play-button').hide();
    });

    $('#lotteryModal').on('show.bs.modal', function() {
        if (isStopButtonShow) {
            intervalId = start();
        }
        if (award_times > 0) {
            hideWinners();
        }
    });

    $('#lotteryModal').on('shown.bs.modal', function() {
        $('#play-button').parent().addClass('shown');
        $('#play-button').hide();
        $('.operate-button').show();
    });

    $('input.award-prize').on('click', function(e) {
        e.stopPropagation();
    });

    $('input.award-prize').on('focusout', function(e) {
        var awardID = $(this).attr('data-award');
        var value = $(this).val();
        $.post(site_url + 'lottery/award/' + awardID + '/update/', {
            'prize': value
        }, function(data) {
            // to do
        }, 'json');
    });

    $(window).on('resize', function() {
        setTimeout(function() {
            adjustWidthFowWinner();
        }, 300);

    });


    initAvatar();
    awardFadeOut();
});
