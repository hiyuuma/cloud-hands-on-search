"""T2: 横断リンクのテスト"""


def test_fargate_plan_linked_to_aws(records):
    plan = next(r for r in records if r["id"] == "plan:HO-SAMPLE-003")
    aws = next(
        r
        for r in records
        if r["source_catalog"] == "aws"
        and r["title"]
        == "Deploy and Scale Containerized Applications with AWS Fargate"
    )
    assert aws["id"] in plan["related"]
    assert plan["id"] in aws["related"]


def test_related_is_bidirectional_id_list(records):
    by_id = {r["id"]: r for r in records}
    for r in records:
        for rid in r["related"]:
            assert rid in by_id
            assert r["id"] in by_id[rid]["related"]
            assert by_id[rid]["source_catalog"] != r["source_catalog"]


def test_no_merge_and_raw_preserved(records):
    # 削除・マージしない: vendor 1582 + plan 3 が全件残る
    assert len(records) == 1585
    for r in records:
        assert isinstance(r["raw"], dict)
