all: linter tests

linter:
	flake8 demucs
	mypy demucs

tests: test_train test_eval

test_train: tests/musdb
	_DORA_TEST_PATH=/tmp/demucs python3 -m dora run --clear \
		dset.musdb=./tests/musdb dset.segment=4 dset.shift=2 epochs=2 model=demucs \
		demucs.depth=2 demucs.channels=4 test.sdr=false misc.num_workers=0 test.workers=0 \
		test.shifts=0

test_eval:
	python3 -m demucs -n demucs_unittest test.mp3
	python3 -m demucs -n demucs_unittest --two-stems=vocals test.mp3
	python3 -m demucs -n demucs_unittest --mp3 test.mp3
	python3 -m demucs -n demucs_unittest --int24 --clip-mode clamp test.mp3

tests/musdb:
	test -e tests || mkdir tests
	python3 -c 'import musdb; musdb.DB("tests/tmp", download=True)'
	musdbconvert tests/tmp tests/musdb

dist:
	python3 setup.py sdist

clean:
	rm -r dist build *.egg-info

.PHONY: linter dist test_train test_eval

#254b0174
ori_ke:
    export CUDA_VISIBLE_DEVICES=1
    pkill -9 -f dora
    dora run dset.musdb=/mnt/sda/shane/projects/my-demucs/ke_ori_dset/ batch_size=4 dset.name=ke test.every=100 epochs=1000 model=hdemucs max_batches=10000
