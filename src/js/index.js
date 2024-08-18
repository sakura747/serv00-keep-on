$(function () {
    var $game = $(".game-container");
    var top = 0;
    var speed = 2;
    var domMove, timer, countTime;
    var totalY = $(".game").offset().top;

    // Create a new game page
    var createDom = function () {
        var $content = $(
            `<div class="game-page">
                <div class="row1">
                    <div class="cell1"></div>
                    <div class="cell2"></div>
                    <div class="cell3"></div>
                    <div class="cell4"></div>
                </div>
                <div class="row2">
                    <div class="cell1"></div>
                    <div class="cell2"></div>
                    <div class="cell3"></div>
                    <div class="cell4"></div>
                </div>
                <div class="row3">
                    <div class="cell1"></div>
                    <div class="cell2"></div>
                    <div class="cell3"></div>
                    <div class="cell4"></div>
                </div>
                <div class="row4">
                    <div class="cell1"></div>
                    <div class="cell2"></div>
                    <div class="cell3"></div>
                    <div class="cell4"></div>
                </div>
            </div>`
        );

        // Randomly mark one cell per row as no-click
        $content.children().each(function () {
            var v = Math.ceil(Math.random() * 4);
            $(this).children(".cell" + v).addClass("no-click");
        });

        $game.prepend($content);
    };

    // Move the game container
    var move = function () {
        timer = setInterval(function () {
            top = $game.position().top;
            top = (top + speed >= 0) ? 0 : top + speed;
            $game.css("top", top);

            if (top >= 0) {
                createDom();
                $game.css("top", "-460px");
            }

            if ($game.children().length >= 3) {
                $game.children().eq(-1).remove();
            }
        }, 20);
    };

    // End the game
    var gameOver = function ($this) {
        clearInterval(domMove);
        clearInterval(timer);
        clearInterval(countTime);
        $this.addClass("error");

        setTimeout(function () {
            alert("Game Over!\nYour score is " + $(".score span").text());
            $(".end-page").fadeIn(500);
            $game.html("");
            $(".timing").hide();
        }, 500);
    };

    // Initialize events
    var initEvents = function () {
        $(".start-btn").click(function () {
            $(".begin-page").fadeOut(500);
            move();
            listener();
            timing();
        });

        $(".restart-btn").click(function () {
            $(".end-page").fadeOut(500);
            move();
            $(".score span").text(0);
            $(".timing p").text(0);
            listener();
            timing();
        });

        $game.on("click", ".cell1, .cell2, .cell3, .cell4", click);
    };

    // Handle cell clicks
    var click = function () {
        if ($(this).hasClass("no-click")) {
            $(this).removeClass("no-click").addClass("clicked");
            var sc = parseInt($(".score span").text());
            $(".score span").text(sc + 1);

            if (sc > 0 && sc % 8 === 0) {
                speed += 1;
            }
        } else {
            gameOver($(this));
        }
    };

    // Monitor unclicked cells
    var listener = function () {
        domMove = setInterval(function () {
            $(".no-click").each(function () {
                var y = $(this).offset().top - totalY;
                if (y >= 362) {
                    gameOver($(this));
                }
            });
        }, 100);
    };

    // Update timing
    var timing = function () {
        $(".timing").show();
        var t1 = new Date().getTime();
        countTime = setInterval(function () {
            var t2 = new Date().getTime();
            var t = t2 - t1;
            var mseconds = parseInt(t % 1000);
            var seconds = parseInt(t / 1000);
            var str = seconds + '.' + mseconds;
            $(".timing p").text(str);
        }, 1);
    };

    initEvents();
    createDom();
});
