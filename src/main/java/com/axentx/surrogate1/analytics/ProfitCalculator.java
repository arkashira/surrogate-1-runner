import com.axentx.surrogate1.api.AccountingSoftware;
import com.axentx.surrogate1.api.Margins;

public class ProfitCalculator {
    private final AccountingSoftware accountingSoftware;

    public ProfitCalculator(AccountingSoftware accountingSoftware) {
        this.accountingSoftware = accountingSoftware;
    }

    public Margins calculateMargins() {
        // Assuming accountingSoftware.getDailyTransactions() returns a list of transactions
        // and accountingSoftware.getWeeklyTransactions() returns a list of weekly transactions
        double dailyRevenue = accountingSoftware.getDailyTransactions().stream()
                .mapToDouble(transaction -> transaction.getAmount())
                .sum();
        double weeklyRevenue = accountingSoftware.getWeeklyTransactions().stream()
                .mapToDouble(transaction -> transaction.getAmount())
                .sum();

        double dailyExpenses = accountingSoftware.getDailyTransactions().stream()
                .filter(transaction -> transaction.getType() == TransactionType.EXPENSE)
                .mapToDouble(transaction -> transaction.getAmount())
                .sum();
        double weeklyExpenses = accountingSoftware.getWeeklyTransactions().stream()
                .filter(transaction -> transaction.getType() == TransactionType.EXPENSE)
                .mapToDouble(transaction -> transaction.getAmount())
                .sum();

        double dailyProfit = dailyRevenue - dailyExpenses;
        double weeklyProfit = weeklyRevenue - weeklyExpenses;

        double dailyMargin = (dailyProfit / dailyRevenue) * 100;
        double weeklyMargin = (weeklyProfit / weeklyRevenue) * 100;

        return new Margins(dailyMargin, weeklyMargin);
    }
}

// src/main/java/com/axentx/surrogate1/api/Margins.java
public class Margins {
    private final double dailyMargin;
    private final double weeklyMargin;

    public Margins(double dailyMargin, double weeklyMargin) {
        this.dailyMargin = dailyMargin;
        this.weeklyMargin = weeklyMargin;
    }

    public double getDailyMargin() {
        return dailyMargin;
    }

    public double getWeeklyMargin() {
        return weeklyMargin;
    }
}

// src/main/java/com/axentx/surrogate1/api/AccountingSoftware.java
public interface AccountingSoftware {
    List<Transaction> getDailyTransactions();
    List<Transaction> getWeeklyTransactions();
}

// src/main/java/com/axentx/surrogate1/api/Transaction.java
public class Transaction {
    private final double amount;
    private final TransactionType type;

    public Transaction(double amount, TransactionType type) {
        this.amount = amount;
        this.type = type;
    }

    public double getAmount() {
        return amount;
    }

    public TransactionType getType() {
        return type;
    }
}

// src/main/java/com/axentx/surrogate1/api/TransactionType.java
public enum TransactionType {
    INCOME,
    EXPENSE
}