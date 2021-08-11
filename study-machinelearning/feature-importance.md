# SMS Features 생성 후 해당 변수의 중요도를 선형적으로 판단하는 방법

## Step 1: Label을 만든다

## Step 2: Feature 또는 Set of Features를 만든다

## Step 3: Feature의 종류를 numeric / categorical / ordinal로 구분한다
- numeric: 수치형  (예) 나이
- categorical: (순서가 없는) 범주형   (예) kyc_type
- ordinal: (순서가 있는) 범주형   (예) 교육수준

## Step 4: Numeric features인 경우, 적당한 [missing value imputation] 한 후, Pearson Correlation을 구한다.
- 적당한 missing value imputation은 예를 들면 다음과 같다.
- 나이가 결측인 경우엔, 나이의 median
- 위도 경도가 결측인 경우엔, 위도 경도의 평균값
- sms transaction amount가 결측인 경우엔, 0
##### 절대값이 크면 클수록 좋은 피쳐이다.

## Step 5: Categorical features인 경우, [missing value imputation] 을 새로운 범주 'NA'를 추가한 후, Pearson's chi-squre test의 p-value를 구한다.
##### 값이 작으면 작을수록 좋은 피쳐이다.

## Step 6: Ordinal features인 경우, [missing value imputation] 을 median으로 수행한 후, Spearman correlation을 구한다.
##### 절대값이 크면 클수록 좋은 피쳐이다.

[missing value imputation]: missing-value-imputation.md