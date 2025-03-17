#!/bin/bash

# 檢查是否在虛擬環境中
if [ -z "$VIRTUAL_ENV" ]; then
    echo "正在啟動虛擬環境..."
    source venv/bin/activate
fi

# 檢查 App3.py 是否正在運行
if pgrep -f "python App3.py" > /dev/null; then
    echo "App3.py 正在運行中..."
else
    echo "正在啟動 App3.py..."
    python App3.py &
    # 等待應用程序啟動
    sleep 5
fi

# 運行測試
echo "開始運行測試..."
pytest test_app.py -v

# 保存測試結果
TEST_RESULT=$?

# 如果 App3.py 是由我們啟動的，則關閉它
if pgrep -f "python App3.py" > /dev/null; then
    pkill -f "python App3.py"
fi

# 返回測試結果
exit $TEST_RESULT 