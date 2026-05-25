# run_all.py
import unittest
import os
import sys
import importlib.util

def run_all_tests():
    # 1. 軸はプロジェクトルートのみ。余計なパスは一切混ぜない
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    #end if

    print("==================================================")
    print(" BeautifulLiner - Running All Unit Tests")
    print("==================================================")

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    test_dir = os.path.join(project_root, "test")

    # 2. ファイルシステムから直接テストモジュールとして読み込む
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                file_path = os.path.join(root, file)
                
                # モジュール名が衝突しないよう、ユニークな仮名（ファイル名ベース）にする
                module_name = os.path.splitext(file)[0]
                
                try:
                    # ファイルパスから直接モジュールをインポートする仕組み
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        # ロードされたモジュールからテストを抽出して追加
                        loaded_suite = loader.loadTestsFromModule(module)
                        suite.addTest(loaded_suite)
                    #end if
                except Exception as e:
                    print(f"Failed to load test file: {file}")
                    print(e)
                #end try
            #end if
        #end for
    #end for

    # 3. 実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if not result.wasSuccessful():
        sys.exit(1)
    #end if
#end def

if __name__ == "__main__":
    run_all_tests()
#end if