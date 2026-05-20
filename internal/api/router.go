package api

import (
	"github.com/gorilla/mux"
)

func NewRouter() *mux.Router {
	r := mux.NewRouter().StrictSlash(true)

	// Mesh endpoint
	mh := NewMeshHandler()
	mh.RegisterRoutes(r)

	// OpenAPI spec + UI
	oh := NewOpenAPIHandler()
	oh.RegisterRoutes(r)

	// Serve static Swagger UI (bundled in ./docs/swagger-ui)
	r.PathPrefix("/docs/").Handler(http.StripPrefix("/docs/", http.FileServer(http.Dir("./docs/swagger-ui"))))

	return r
}