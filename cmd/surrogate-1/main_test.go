package main

import (
	"reflect"
	"testing"
)

func TestParseReposFlag(t *testing.T) {
	tests := []struct {
		name    string
		args    []string
		want    []string
		wantErr bool
	}{
		{
			name: "single repo",
			args: []string{"--repos=repo1"},
			want: []string{"repo1"},
		},
		{
			name: "multiple repos with spaces",
			args: []string{"--repos=repo1, repo2 ,repo3"},
			want: []string{"repo1", "repo2", "repo3"},
		},
		{
			name: "empty repos flag",
			args: []string{"--repos="},
			want: []string{},
		},
		{
			name: "no repos flag",
			args: []string{},
			want: []string{},
		},
		{
			name:    "invalid flag syntax",
			args:    []string{"--repos"},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ParseReposFlag(tt.args)
			if (err != nil) != tt.wantErr {
				t.Fatalf("ParseReposFlag() error = %v, wantErr %v", err, tt.wantErr)
			}
			if !reflect.DeepEqual(got, tt.want) {
				t.Fatalf("ParseReposFlag() = %v, want %v", got, tt.want)
			}
		})
	}
}