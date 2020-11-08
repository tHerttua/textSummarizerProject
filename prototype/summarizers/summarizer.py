from pytldr.summarize import TextRankSummarizer
from pytldr.summarize.lsa import LsaOzsoy, LsaSteinberger
from pytldr.summarize import RelevanceSummarizer

def textRank(text, refSentences=5):
    TextRankSum = TextRankSummarizer()
    summary_TextRank = TextRankSum.summarize(text, length=refSentences)
    return summary_TextRank

def LSA_O(text, refSentences=5):
    LSAOSum = LsaOzsoy()
    o_summary = LSAOSum.summarize(text, topics=4, length=refSentences, binary_matrix=True, topic_sigma_threshold=0.5)
    return o_summary

def LSA_S(text, refSentences=5):
    LSASSum = LsaSteinberger()
    s_summary = LSASSum.summarize(text, topics=4, length=refSentences, binary_matrix=True, topic_sigma_threshold=0.5)
    return s_summary

def relevance(text, refSentences=5):
    RelevanceSum = RelevanceSummarizer()
    summary_relevance = RelevanceSum.summarize(text, length=refSentences, binary_matrix=True)
    return summary_relevance

