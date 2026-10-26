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
{{-$ipv4Regex="(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"-}}
{{-$ipv6Regex="^(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:))$"-}}
{{-$ipv6BracketedRegex="^\[(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:))\]$"-}}
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
ip: {{ $hostname | quote}}
fqdn: ""
{{-  else-}}
{{-    if or (regexMatch $ipv6Regex $hostname) (regexMatch $ipv6BracketedRegex $hostname)-}}
type: "ipv6"
ip: {{ $hostname | quote}}
fqdn: ""
{{-    else-}}
type: "fqdn"
ip: ""
fqdn: {{ $hostname | quote}}
{{-    end-}}
{{-  end-}}
ports:
  {{ toYaml $ports | nident 2}}
path: {{$urlDetails.path}}
query: {{$urlDetails.query}}
fragment: {{$urlDetails.fragment}}
{{-end-}}

{{-define "practice-project.netpol.svcLookup"-}}
{{-$hostname:=index . 0-}}
{{-$values:=index . 1-}}
{{-$clusterDomain:=(default "cluster.local" $values.global.clusterDomain)-}}
{{-$regexShort:="^([a-zA-z0-9\-\_])+$"-}}
{{-$regexNamespaced:="^([a-zA-z0-9\-\_])+\.([a-zA-z0-9\-\_])+$"-}}
{{-$regexFull:=(print "^([a-zA-z0-9\-\_])+\.([a-zA-z0-9\-\_])+\.svc\." $clusterDomain "$")-}}
{{-if regexMatch $regexShort $hostname-}}
{{-$details:=lookup "v1" "Service" $values.Release.Namespace (index (split $url ".") 0) }}
{{-if and (eq $details.type "ClusterIP") $details.clusterIP -}}
- ipBlock:
    cidr: {{$details.clusterIP | quote }}
{{-end-}}
- podSelector:
    matchLabel:
    {{ toYaml $details.spec.selector | nident 4 }}
{{-else-}}
{{-  if or (regexMatch $regexNamespaced $hostname) (regexMatch $regexFull $hostname)-}}
{{-$details:=lookup "v1" "Service"  (index (split $url ".") 1) (index (split $url ".") 0) }}
{{-if and $values.networkPolicy.useClusterIPForFqdn (eq $details.type "ClusterIP") $details.clusterIP -}}
- ipBlock:
    cidr: {{$details.clusterIP | quote }}
{{-end-}}
- podSelector:
    matchLabel:
      {{ toYaml $details.spec.selector | nident 4 }}
  namespaceSelector:
    matchLabel:
      kubernetes.io/metadata.name: {{(index (split $url ".") 1) | quote}}
{{-else-}}
{{-if  $values.networkPolicy.useDnsForFqdn -}}
{{- with (getHostByName $url)-}}
- ipBlock:
    cidr: {{ . | quote}}
{{- end-}}
{{- end-}}
{{-end-}}
{{-end-}}