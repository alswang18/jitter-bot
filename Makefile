.PHONY: setup
setup:
	pip install -r requirements.txt
	echo Enter discord bot key: 
	read discord_bot_key
	echo Enter symbl ai key:
	read symbl_ai_key
	export DISCORD_TOKEN=$$discord_bot_key
	export SYMBOL_KEY=$$symbl_ai_key

.PHONY: run
run:
	python main.py