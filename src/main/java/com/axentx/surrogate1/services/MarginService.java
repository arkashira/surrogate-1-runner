import com.axentx.surrogate1.analytics.ProfitCalculator;
import com.axentx.surrogate1.api.AccountingSoftware;

public class MarginService {
    private final ProfitCalculator profitCalculator;
    private final AccountingSoftware accountingSoftware;

    public MarginService(ProfitCalculator profitCalculator, AccountingSoftware accountingSoftware) {
        this.profitCalculator = profitCalculator;
        this.accountingSoftware = accountingSoftware;
    }

    public Margins getMargins() {
        return profitCalculator.calculateMargins();
    }
}