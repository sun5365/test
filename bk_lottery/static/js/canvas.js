$(function() {
    var avatarCounts = 600;
    var avatarDepth = 100;
    var sizeFactor = 6;
    var windowWidth = 600;
    var windowHeight = 400;
    var speed = 4;
    var zRange = 400;
    var xRange = 600;
    var yRange = 400;
    var image = document.getElementById('image');
    var isStop = false;
    var isClick = false;
    var isLast = false;

    var canvas = document.getElementById('space');
    var context = canvas.getContext('2d');
    context.globalAlpha = 0.6;

    var avatars = [];
    initRandomCoordinate(avatars);

    function initRandomCoordinate() {
        for (var i = 0; i < avatarCounts; i++) {
            // [xcoordinate, ycoordinate, zcoordinate]
            avatar = [(Math.random() * xRange) - xRange / 2, (Math.random() * yRange) - yRange / 2, (Math.random() * zRange) - zRange / 2];
            avatars.push(avatar);
        }
    }

    function render() {
        context.fillStyle = '#00113F';
        context.fillRect(0, 0, windowWidth, windowHeight);

        for (var i = 0; i < avatarCounts; i++) {
            var z3D = avatars[i][2];
            z3D -= speed;
            if (z3D < -avatarDepth) {
                z3D += zRange;
            }
            avatars[i][2] = z3D;
            var avatar = avatars[i];

            if (isClick && i === 0) {
                draw3Din2D(avatar, true);
            } else {
                if (isStop) {
                    return;
                }
                draw3Din2D(avatar, false);
            }
        }
    }

    function draw3Din2D(avatar3D, isWinner) {
        var x3D = avatar3D[0];
        var y3D = avatar3D[1];
        var z3D = avatar3D[2];
        var scale = avatarDepth / (avatarDepth + z3D);
        var x2D = (x3D * scale) + xRange / 2;
        var y2D = (y3D * scale) + yRange / 2;

        if (isWinner) {
            // make the avatar in the middle of the window
            var temp = scale * sizeFactor / 2;
            if (scale * sizeFactor > 100) {
                isStop = true;
                context.globalAlpha = 1.0;
            }
            if (isStop) {
                clearInterval(intervalId);
            }
            context.drawImage(image, x2D - temp, y2D - temp, scale * sizeFactor, scale * sizeFactor);
        } else {
            context.drawImage(image, x2D, y2D, scale * sizeFactor, scale * sizeFactor);
        }
    }

    function start() {
        return setInterval(function() {
            render(context, avatars);
        }, 50);
    }

    var intervalId = start();

    $('#stop').click(function() {
        avatars[0] = [0,0,0];
        isClick = true;
    });
});