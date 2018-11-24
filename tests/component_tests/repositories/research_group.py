class ResearchGroupRepository:
    def __init__(self):
        self._research_groups = {}

    def get_research_group(self, research_group_id):
        if research_group_id in self._research_groups:
            return self._research_groups[research_group_id]

    def save(self, research_group):
        self._research_groups[research_group.id] = research_group
