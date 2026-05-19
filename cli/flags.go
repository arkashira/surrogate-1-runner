package cli

import (
	"github.com/spf13/cobra"
)

func NewFlags() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "surrogate-1",
		Short: "A brief description of your application",
	}

	cmd.PersistentFlags().Bool("validate", false, "Run a validation check on AI-generated code")

	return cmd
}