package main

import (
	"context"
	"fmt"
	"github.com/databricks/terraform-provider-databricks/databricks"
	"github.com/hashicorp/terraform-plugin-sdk/v2/diag"
	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/schema"
)

func importDatabricksResource(d *schema.ResourceData, meta interface{}) ([]diag.Diagnostic, error) {
	config := meta.(*databricks.Client).Config
	workspaceID := config.WorkspaceID

	// API calls to Databricks include the correct workspace_id in the request path
	resourceID := d.Id()
	resourcePath := fmt.Sprintf("/api/2.0/workspace/attachments/%s/%s", workspaceID, resourceID)

	// Implement the import logic using the resourcePath
	// ...

	return nil, nil
}