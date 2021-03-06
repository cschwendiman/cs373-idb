FILES :=                     \
    .gitignore               \
    makefile                 \
    apiary.apib              \
    IDB3.log                 \
    models.py                \
    model.html               \
    tests.py                 \
    UML.pdf

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -rf __pycache__
	rm -f *.tmp

test: tweetcity-test.tmp

model.html: models.py
	pydoc -w models

IDB3.log:
	git log > IDB3.log

tweetcity-test.tmp: tests.py
	coverage3 run    --branch tests.py >  tweetcity-test.tmp 2>&1
	coverage3 report -m                      >> tweetcity-test.tmp
	cat tweetcity-test.tmp
