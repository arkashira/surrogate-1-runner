class ExplanationFormatter:
    @staticmethod
    def format_explanation(charge_type, charge_amount, service_name, additional_info=None):
        if charge_type == "setup_fee":
            return InvoiceExplanationPrompts.generate_setup_fee_prompt(charge_amount, service_name)
        elif charge_type == "subscription_fee":
            return InvoiceExplanationPrompts.generate_subscription_fee_prompt(charge_amount, service_name)
        elif charge_type == "usage_fee":
            return InvoiceExplanationPrompts.generate_usage_fee_prompt(charge_amount, service_name, additional_info)
        elif charge_type == "discount":
            return InvoiceExplanationPrompts.generate_discount_prompt(charge_amount, additional_info)
        else:
            return "Charge type not recognized."