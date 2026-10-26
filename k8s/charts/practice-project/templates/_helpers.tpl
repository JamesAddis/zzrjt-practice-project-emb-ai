{{/*
Expand the name of the chart.
*/}}
{{- define "practice-project.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "practice-project.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "practice-project.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "practice-project.labels" -}}
helm.sh/chart: {{ include "practice-project.chart" . }}
{{ include "practice-project.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "practice-project.selectorLabels" -}}
app.kubernetes.io/name: {{ include "practice-project.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "practice-project.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "practice-project.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{-define "practice-project.route"-}}
{{-$ipv4Regex=""-}}
{{-$ipv6Regex=""-}}
{{-$ipv6PortRegex=""-}}
{{-$portRegex:="^(?:.+):(\d+)$"-}}
{{-$urlDetails:=urlParse .-}}
{{-$hostname:=$urlDetails.host-}}
{{-ports:=(list 80 443)-}}
{{-if regexMatch $portRegex $hostname-}}
{{-  $hostname:= index (split $urlDetails.host ":") 0-}}
{{-  $ports =(list (index (split $urlDetails.host ":") 1))-}}
{{-else-}}
{{-  if has $urlDetails.scheme (list "http" "ws")-}}
{{-    $ports =(list 80)-}}
{{-  else-}}
{{-    if has $urlDetails.scheme (list "https" "wss")-}}
{{-      $ports =(list 443)-}}
{{-    end-}}
{{-  end-}}
{{-  if (regexMatch $ipv4Regex $hostname)-}}
type: "ipv4"
fqdn: {{ $hostname | quote}}
{{-  else-}}
{{-    if or (regexMatch $ipv6Regex $hostname) (regexMatch $ipv6BracketRegex $hostname)-}}
type: "ipv6"
ip: {{ $hostname | quote}}
{{-    else-}}
type: "fqdn"
fqdn: {{ $hostname | quote}}
{{-    end-}}
{{-  end-}}
ports:
  {{ toYaml $ports | nident 2}}
path: {{$urlDetails.path}}
query: {{$urlDetails.query}}
fragment: {{$urlDetails.fragment}}
{{-end-}}