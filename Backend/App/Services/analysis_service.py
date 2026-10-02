from app.engine.recommendation import RecommendationModule
from app.repositories.line_item_repository import LineRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.models.recommendation import Recommendation

class AnalysisService : 
    def __init__(self,db):
        self.line_repo = LineRepository(db)
        self.recommendation_repo = RecommendationRepository(db)
        self.recommendation_module = RecommendationModule()

    def analyze_statement(self, company_id, statement_id):
        # line repo
        saved_items = self.line_repo.get_by_statement(statement_id)
        data = {item.standardized_label : item.value for item in saved_items}
        result = self.recommendation_module.run(data)
        recommendation = self.recommendation_repo.create(Recommendation(
            company_id = company_id,
            statement_id = statement_id,
            recommended_action = result.values.get("recommended_action"),
            supporting_metrics = result.values,
        ))

        return recommendation
    
         


        
