[![make.fun](https://make.fun/badge/u-tuan-muda-one-word-for-your-wi-fi-a1b4fd72.svg)](https://make.fun/bounty/u-tuan-muda-one-word-for-your-wi-fi-a1b4fd72)
[![rank](https://make.fun/badge/u-tuan-muda-one-word-for-your-wi-fi-a1b4fd72/Bradestudio/u-tuan-muda-one-word-for-your-wi-fi-a1b4fd72/rank.svg)](https://make.fun/bounty/u-tuan-muda-one-word-for-your-wi-fi-a1b4fd72)
[![reward](https://make.fun/badge/u-tuan-muda-one-word-for-your-wi-fi-a1b4fd72/Bradestudio/u-tuan-muda-one-word-for-your-wi-fi-a1b4fd72/reward.svg)](https://make.fun/bounty/u-tuan-muda-one-word-for-your-wi-fi-a1b4fd72)

# One Word for Your Wi-Fi

A [make.fun](https://make.fun/bounty/u-tuan-muda-one-word-for-your-wi-fi-a1b4fd72) entry: one word describing my Wi-Fi, aiming to be the funniest and most accurate.

## The entry

> Politician

It promises five bars and delivers one — all talk, no signal. As a network name it is the joke itself.

## Run

```sh
python3 main.py
```

The program writes the single word to `/output/entry.txt` (or `$OUTPUT_DIR/entry.txt` when set), atomically via a temp file plus rename, fsyncs the file and its directory, then reads it back byte-for-byte to verify it. It prints the character count (10).

`main.py` is standard library only, makes no network calls, and reads no files outside the program.
