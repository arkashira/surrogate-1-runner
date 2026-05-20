class InvoiceExplanationPrompts:
    @staticmethod
    def generate_setup_fee_prompt(charge_amount, service_name):
        return f"The charge of ${charge_amount} is a setup fee for {service_name}."

    @staticmethod
    def generate_subscription_fee_prompt(charge_amount, service_name):
        return f"The charge of ${charge_amount} is a subscription fee for {service_name}."

    @staticmethod
    def generate_usage_fee_prompt(charge_amount, service_name, usage_details):
        return f"The charge of ${charge_amount} is based on your usage of {service_name}. Details: {usage_details}."

    @staticmethod
    def generate_discount_prompt(discount_amount, original_amount):
        return f"You received a discount of ${discount_amount} from your original charge of ${original_amount}."