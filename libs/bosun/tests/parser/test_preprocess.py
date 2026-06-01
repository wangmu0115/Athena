from athena_bosun.parser.preprocess import preprocess

raw_bosun_str1 = """
$empty_qps= nv(avg(q("sum:rate{counter}:ecom.sophon.feed.RecommendSourceQPS{block_name=not_literal_or(favorite_order_detail|product_recommend_banner|coupon_shops),scene_name=*}{recommend_count=0}", "2m", "1m")),0)
$uid0_qps= nv(avg(q("sum:rate{counter}:ecom.feed.channel.CommonFeedParams{block_name=not_literal_or(favorite_order_detail|product_recommend_banner|coupon_shops),scene_name=*}{has_uid=false}", "2m", "1m")),0)

warn =  $empty_qps - $uid0_qps > 100
runEvery=1
"""

print(preprocess(raw_bosun_str1))
