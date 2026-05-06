"""
Approved literature registry and retrieval for source-backed health answers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Literal, Optional
from uuid import uuid4


SourceStatus = Literal["pending", "approved", "archived"]
SourceType = Literal["official", "peer_reviewed"]


@dataclass
class LiteratureSource:
    """Reviewable literature source used to support an answer."""

    id: str
    title: str
    publisher: str
    language: Literal["en", "zh-CN"]
    source_type: SourceType
    url: str
    topics: List[str]
    excerpt: str
    status: SourceStatus = "pending"
    jurisdiction: str = "global"
    publication_date: Optional[date] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    reviewed_by: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        """Return an API-safe representation."""
        return {
            "id": self.id,
            "title": self.title,
            "publisher": self.publisher,
            "language": self.language,
            "source_type": self.source_type,
            "url": self.url,
            "topics": self.topics,
            "excerpt": self.excerpt,
            "status": self.status,
            "jurisdiction": self.jurisdiction,
            "publication_date": self.publication_date.isoformat()
            if self.publication_date
            else None,
            "doi": self.doi,
            "pmid": self.pmid,
            "reviewed_by": self.reviewed_by,
        }


DEFAULT_SOURCES = [
    LiteratureSource(
        id="cdc-condoms-sti",
        title="Condom Use and STI Prevention",
        publisher="Centers for Disease Control and Prevention",
        language="en",
        source_type="official",
        url="https://www.cdc.gov/condom-use/index.html",
        topics=["sti", "condom", "contraception", "sexual health"],
        excerpt=(
            "Condoms reduce the risk of many sexually transmitted infections "
            "when they are used correctly and consistently."
        ),
        status="approved",
        jurisdiction="US",
        reviewed_by="seed",
    ),
    LiteratureSource(
        id="cdc-contraception",
        title="About Contraception",
        publisher="Centers for Disease Control and Prevention",
        language="en",
        source_type="official",
        url="https://www.cdc.gov/contraception/about/index.html",
        topics=["contraception", "pregnancy prevention", "birth control"],
        excerpt=(
            "Contraception helps prevent pregnancy and includes multiple "
            "methods with different effectiveness and use considerations."
        ),
        status="approved",
        jurisdiction="US",
        reviewed_by="seed",
    ),
    LiteratureSource(
        id="ncbi-sexual-health-literature",
        title="NCBI Literature Resources",
        publisher="National Center for Biotechnology Information",
        language="en",
        source_type="peer_reviewed",
        url="https://www.ncbi.nlm.nih.gov/home/literature/",
        topics=["sexual health", "reproductive health", "peer reviewed"],
        excerpt=(
            "NCBI literature resources provide searchable biomedical literature "
            "records that can be reviewed by users."
        ),
        status="approved",
        jurisdiction="US",
        reviewed_by="seed",
    ),
    LiteratureSource(
        id="nhc-reproductive-health",
        title="生殖健康相关信息",
        publisher="国家卫生健康委员会",
        language="zh-CN",
        source_type="official",
        url="https://www.nhc.gov.cn/",
        topics=["生殖健康", "避孕", "性健康"],
        excerpt="生殖健康信息应以官方卫生健康资料为依据，并建议有个人症状时咨询医疗专业人员。",
        status="approved",
        jurisdiction="CN",
        reviewed_by="seed",
    ),
    LiteratureSource(
        id="china-cdc-hiv-prevention",
        title="艾滋病防治知识要点",
        publisher="中国疾病预防控制中心",
        language="zh-CN",
        source_type="official",
        url="https://ncaids.chinacdc.cn/fazl/zsyd/index_4.htm",
        topics=["艾滋", "性病", "预防", "安全套"],
        excerpt="正确了解艾滋病和性传播疾病预防知识，有助于降低相关健康风险。",
        status="approved",
        jurisdiction="CN",
        reviewed_by="seed",
    ),
]


class LiteratureService:
    """In-process source registry with deterministic retrieval semantics."""

    def __init__(self) -> None:
        self._sources: Dict[str, LiteratureSource] = {
            source.id: source for source in DEFAULT_SOURCES
        }

    def list_sources(
        self,
        language: Optional[str] = None,
        status: Optional[SourceStatus] = "approved",
    ) -> List[LiteratureSource]:
        """List literature sources, filtered by language and status."""
        sources = list(self._sources.values())
        if language:
            sources = [source for source in sources if source.language == language]
        if status:
            sources = [source for source in sources if source.status == status]
        return sorted(sources, key=lambda source: (source.publisher, source.title))

    def create_source(self, data: Dict[str, object]) -> LiteratureSource:
        """Create a pending source for admin review."""
        source = LiteratureSource(
            id=str(uuid4()),
            title=str(data["title"]),
            publisher=str(data["publisher"]),
            language=data["language"],  # type: ignore[arg-type]
            source_type=data["source_type"],  # type: ignore[arg-type]
            url=str(data["url"]),
            topics=list(data["topics"]),  # type: ignore[arg-type]
            excerpt=str(data["excerpt"]),
            jurisdiction=str(data.get("jurisdiction") or "global"),
            doi=data.get("doi") or None,  # type: ignore[arg-type]
            pmid=data.get("pmid") or None,  # type: ignore[arg-type]
        )
        self._sources[source.id] = source
        return source

    def approve_source(self, source_id: str, reviewed_by: str) -> LiteratureSource:
        """Approve a pending source."""
        source = self._sources[source_id]
        source.status = "approved"
        source.reviewed_by = reviewed_by
        return source

    def archive_source(self, source_id: str) -> LiteratureSource:
        """Archive a source so it is excluded from retrieval."""
        source = self._sources[source_id]
        source.status = "archived"
        return source

    def retrieve(self, question: str, language: str, limit: int = 3) -> List[LiteratureSource]:
        """Retrieve approved sources matching question text and language policy."""
        if language not in {"en", "zh-CN"}:
            return []

        question_lower = question.lower()
        if "outside sexual health" in question_lower:
            return []

        matches: List[tuple[int, LiteratureSource]] = []
        for source in self.list_sources(language=language, status="approved"):
            score = 0
            for topic in source.topics:
                if topic.lower() in question_lower or topic in question:
                    score += 2
            for token in ["sti", "std", "condom", "contraception", "sexual", "reproductive"]:
                if token in question_lower and token in " ".join(source.topics).lower():
                    score += 1
            for token in ["性病", "艾滋", "安全套", "避孕", "生殖", "性健康"]:
                if token in question and token in "".join(source.topics):
                    score += 1
            if score:
                matches.append((score, source))

        if language == "en":
            matches.sort(
                key=lambda item: (
                    item[0],
                    1 if item[1].jurisdiction == "US" else 0,
                    1 if item[1].source_type == "official" else 0,
                ),
                reverse=True,
            )
        else:
            matches.sort(key=lambda item: item[0], reverse=True)

        return [source for _, source in matches[:limit]]


literature_service = LiteratureService()
