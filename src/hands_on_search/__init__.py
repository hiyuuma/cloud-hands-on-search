"""cloud-hands-on-search: 3クラウド学習カタログ統合 ETL (T1) と横断リンク (T2)"""

__all__ = ["run_etl", "load_all"]


def __getattr__(name):
    # etl の遅延 import。python -m hands_on_search.etl 実行時に
    # runpy の RuntimeWarning (モジュール二重読み込み) を避けるため。
    if name in __all__:
        from .etl import load_all, run_etl

        return {"run_etl": run_etl, "load_all": load_all}[name]
    raise AttributeError(name)
