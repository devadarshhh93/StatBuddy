import streamlit as st
from google import genai
from google.genai import types

# ------------------------------------------------------------
# StatBuddy: SPSS Statistical Test Selector
# ------------------------------------------------------------

st.set_page_config(
    page_title="StatBuddy | SPSS Test Selector",
    page_icon="📊",
    layout="centered",
)

MANUAL = """
SPSS STATISTICAL TEST SELECTOR - KNOWLEDGE BASE
Based on the UCLA OARC "What statistical analysis should I use? - SPSS" guide.

Demo dataset: hsb2 (200 high-school students)
Variables: female (0/1), ses (1-3), race, schtyp, prog (1-3 program type),
read, write, math, science, socst (scores).

PART 1: THE 3-QUESTION TRICK
Q1. What TYPE is my outcome (dependent) variable?
- Interval/continuous & roughly normal (scores, weight, income logs)
- Ordinal (ranks, Likert, not normal)
- Categorical (yes/no, groups)
Q2. How many GROUPS / VARIABLES do I have, and what type are my predictors?
Q3. Are observations INDEPENDENT or PAIRED/REPEATED (same person measured again)?
Memory trick: DV type -> number of groups -> independent or paired.

PART 2: QUICK DECISION TABLE
ONE SAMPLE:
- Normal interval DV -> One-sample t-test
- Ordinal / not normal DV -> One-sample median test (Wilcoxon)
- 2-level categorical DV (proportion) -> Binomial test
- Categorical DV vs expected % -> Chi-square goodness of fit

TWO INDEPENDENT GROUPS:
- Normal interval DV -> Independent samples t-test
- Ordinal / not normal DV -> Wilcoxon-Mann-Whitney test
- Categorical DV -> Chi-square test (or Fisher's exact if expected cell count < 5)

TWO OR MORE INDEPENDENT GROUPS (1 factor):
- Normal interval DV -> One-way ANOVA
- Ordinal / not normal DV -> Kruskal-Wallis test
- Categorical DV -> Chi-square test

PAIRED / RELATED:
- Normal interval DV -> Paired t-test
- Ordinal / not normal DV -> Wilcoxon signed-rank test
- Only positive/negative differences -> Sign test
- Two binary outcomes (matched) -> McNemar test

REPEATED MEASURES (2+ time points, same subjects):
- Normal interval DV -> One-way repeated measures ANOVA
- Ordinal / not normal DV -> Friedman test
- Binary DV repeated -> Repeated measures logistic regression (GENLIN)

TWO OR MORE FACTORS:
- Normal interval DV -> Factorial ANOVA
- Binary DV -> Factorial logistic regression
- Ordinal DV -> Ordered logistic regression
- Add a continuous covariate -> ANCOVA

RELATIONSHIPS / PREDICTION:
- 2 normal interval variables -> Pearson correlation
- 2 ordinal / non-normal variables -> Spearman correlation
- 1 interval predictor -> 1 interval DV -> Simple linear regression
- Many predictors -> 1 interval DV -> Multiple regression
- 1 predictor -> binary DV -> Simple logistic regression
- Many predictors -> binary DV -> Multiple logistic regression

MULTIVARIATE:
- Interval predictors -> categorical group DV -> Discriminant analysis
- 1 categorical IV, 2+ interval DVs -> One-way MANOVA
- 2+ interval predictors, 2+ interval DVs -> Multivariate multiple regression
- Relationship between TWO SETS of variables -> Canonical correlation
- Reduce many variables to a few factors -> Factor analysis

PART 3: TEST DETAILS, SPSS SYNTAX AND EXAMPLES

1) ONE-SAMPLE T-TEST
Use: Is the sample mean of a normal interval variable different from a fixed value?
SPSS: T-TEST /TESTVAL = 50 /VARIABLE = write.
Menu: Analyze > Compare Means > One-Sample T Test.
Example: Mean write = 52.775 vs 50 -> significantly higher.
Trick: One group + one number to compare against.

2) ONE-SAMPLE MEDIAN TEST (Wilcoxon)
Use: Same as above but variable is only ordinal / not normal.
SPSS: NPTESTS /ONESAMPLE TEST (write) WILCOXON(TESTVALUE = 50).
Trick: Median version of the one-sample t-test.

3) BINOMIAL TEST
Use: Does the proportion of one outcome in a 2-level variable differ from a set value?
SPSS: NPAR TESTS /BINOMIAL (.5) = female.
Example: Proportion of females vs 50% -> p = .229 (not significant).

4) CHI-SQUARE GOODNESS OF FIT
Use: Do observed category proportions differ from expected proportions?
SPSS: NPAR TEST /CHISQUARE = race /EXPECTED = 10 10 10 70.
Example: Expected 10/10/10/70% -> chi-square (df 3) = 5.029, p = .170.

5) INDEPENDENT SAMPLES T-TEST
Use: Compare means of a normal interval DV between 2 independent groups.
SPSS: T-TEST GROUPS = female(0 1) /VARIABLES = write.
Menu: Analyze > Compare Means > Independent-Samples T Test.
Example: Females 54.99 vs males 50.12, t = -3.734, p = .000 -> significant.
Tip: Check Levene's test. Similar SDs (10.3 vs 8.1) -> read equal variances assumed row.

6) WILCOXON-MANN-WHITNEY TEST
Use: Non-parametric alternative to independent t-test (DV at least ordinal).
SPSS: NPAR TEST /M-W = write BY female(0 1).
Example: z = -3.329, p = .001 -> distributions differ.

7) CHI-SQUARE TEST OF INDEPENDENCE
Use: Is there a relationship between two categorical variables?
SPSS: CROSSTABS /TABLES = schtyp BY female /STATISTIC = CHISQ.
Menu: Analyze > Descriptive Statistics > Crosstabs > Statistics > Chi-square.
Examples: school type vs gender -> chi-square(1) = 0.047, p = .828;
female by ses -> chi-square(2) = 4.577, p = .101.
Assumption: every cell's EXPECTED count should be 5 or more.

8) FISHER'S EXACT TEST
Use: Chi-square situation but expected cell count <= 5 (small samples).
SPSS: Given by default for a 2x2 table in Crosstabs (use SPSS Exact Tests module for larger tables).

9) ONE-WAY ANOVA
Use: Compare means of a normal interval DV across 3+ groups of one categorical variable.
SPSS: ONEWAY write BY prog. Group means: MEANS TABLES = write BY prog.
Menu: Analyze > Compare Means > One-Way ANOVA.
Example: write differs by program type; academic highest, vocational lowest.
Tip: A significant ANOVA only says some groups differ - run post hoc tests to find which.

10) KRUSKAL-WALLIS TEST
Use: Non-parametric ANOVA (ordinal DV, 2+ groups).
SPSS: NPAR TESTS /K-W = write BY prog (1,3).
Trick: Mann-Whitney for 3+ groups.

11) PAIRED T-TEST
Use: Two related measurements per subject (before/after, read vs write) on a normal interval variable.
SPSS: T-TEST PAIRS = read WITH write (PAIRED).
Example: t = -0.867, p = .387 -> no significant difference.

12) WILCOXON SIGNED-RANK TEST
Use: Non-parametric paired t-test (difference is ordinal, not normal).
SPSS: NPAR TEST /WILCOXON = write WITH read (PAIRED).

13) SIGN TEST
Use: Paired data where differences can only be classed as positive or negative.
SPSS: NPAR TEST /SIGN = read WITH write (PAIRED).
Example: p = .556 -> no significant difference.

14) MCNEMAR TEST
Use: Two binary outcomes on the same subjects / matched pairs.
SPSS:
COMPUTE himath = (math>60). COMPUTE hiread = (read>60). EXECUTE.
CROSSTABS /TABLES=himath BY hiread /STATISTIC=MCNEMAR /CELLS=COUNT.
Null hypothesis: the two proportions are equal (table is symmetric).

15) ONE-WAY REPEATED MEASURES ANOVA
Use: Same subjects measured 3+ times on a normal interval DV.
SPSS: GLM y1 y2 y3 y4 /WSFACTOR a(4).
Menu: Analyze > General Linear Model > Repeated Measures.
Tip: SPSS prints Sphericity Assumed, Greenhouse-Geisser, Huynh-Feldt, Lower-bound.
If sphericity is violated, use Greenhouse-Geisser or Huynh-Feldt.

16) REPEATED MEASURES LOGISTIC REGRESSION
Use: Binary outcome measured repeatedly on each subject.
SPSS: GENLIN with DISTRIBUTION=BINOMIAL LINK=LOGIT and /REPEATED SUBJECT=id.
Example: Predict high pulse (>100) from diet -> Wald chi-square = 1.562, p = .211.

17) FACTORIAL ANOVA
Use: 2+ categorical IVs, one normal interval DV (can test interaction).
SPSS: GLM write BY female ses.
Tip: SPSS makes the interaction (female*ses) automatically.
Example: female (p = .000) and ses (p = .002) significant; interaction p = .875.

18) FRIEDMAN TEST
Use: Non-parametric repeated measures ANOVA (ordinal DV, 3+ related measures).
SPSS: NPAR TESTS /FRIEDMAN = read write math.
Example: chi-square = 0.645, p = .724 -> no difference.

19) ORDERED (ORDINAL) LOGISTIC REGRESSION
Use: DV is ordered categories (low / medium / high).
SPSS: PLUM write3 WITH female read socst /LINK = LOGIT /PRINT = PARAMETER SUMMARY TPARALLEL.
Key assumption: proportional odds (parallel lines). Non-significant test (p = .563) = assumption OK.
Tip: Avoid turning a continuous variable into categories unless needed.

20) FACTORIAL LOGISTIC REGRESSION
Use: 2+ categorical IVs and a binary (0/1) DV.
SPSS: LOGISTIC REGRESSION female WITH prog schtyp prog BY schtyp /CONTRAST(prog) = INDICATOR(1).
Note: Categorical predictors get dummy codes (indicator contrasts).

21) CORRELATION (Pearson)
Use: Linear relationship between two normal interval variables (dummy 0/1 allowed).
SPSS: CORRELATIONS /VARIABLES = read write.
Menu: Analyze > Correlate > Bivariate.
Example: r(read, write) = 0.597.
Trick: r squared x 100 = % shared variance (0.6^2 = 0.36 -> 36%).

22) SIMPLE LINEAR REGRESSION
Use: Predict one interval DV from one interval predictor.
SPSS: REGRESSION VARIABLES = write read /DEPENDENT = write /METHOD = ENTER.
Menu: Analyze > Regression > Linear.
Example: B = .552, t = 10.47, p = .000 -> significant positive linear relationship.

23) SPEARMAN (NON-PARAMETRIC) CORRELATION
Use: Ordinal or non-normal variables (uses ranks).
SPSS: NONPAR CORR /VARIABLES = read write /PRINT = SPEARMAN.
Example: rho = 0.617, p = .000.

24) SIMPLE LOGISTIC REGRESSION
Use: Binary (0/1) DV, one predictor.
SPSS: LOGISTIC REGRESSION female WITH read.
Rule: first variable after command = outcome; rest after WITH = predictors.
Predictors must be dichotomous or continuous (categorical ones need dummy coding).

25) MULTIPLE REGRESSION
Use: Predict one interval DV from several predictors.
SPSS: REGRESSION VARIABLE = write female read math science socst /DEPENDENT = write /METHOD = ENTER.
Example: Overall F = 58.60, p = .000; all predictors significant except read.

26) ANCOVA
Use: ANOVA + a continuous covariate to adjust for it.
SPSS: GLM write WITH read BY prog.
Example: After adjusting for read, write still differs by program (F = 5.867, p = .003).
Trick: ANOVA + continuous variable after WITH.

27) MULTIPLE LOGISTIC REGRESSION
Use: Binary DV with 2+ predictors.
SPSS: LOGISTIC REGRESSION female WITH read write.

28) DISCRIMINANT ANALYSIS
Use: Predict a categorical group from interval predictors.
SPSS: DISCRIMINATE GROUPS = prog(1, 3) /VARIABLES = read write math.

29) ONE-WAY MANOVA
Use: 1 categorical IV + 2 or more interval DVs.
SPSS: GLM read write math BY prog.
Example: Programs differ in the joint distribution of read, write and math.

30) MULTIVARIATE MULTIPLE REGRESSION
Use: 2+ DVs predicted from 2+ predictors.
SPSS: GLM write read WITH female math science socst.

31) CANONICAL CORRELATION
Use: Relationship between two sets of interval variables (separated by WITH).
SPSS: MANOVA read write WITH math science /DISCRIM.

32) FACTOR ANALYSIS
Use: Find underlying factors / reduce number of variables (interval variables).
SPSS: FACTOR /VARIABLES read write math science socst /CRITERIA FACTORS(2)
 /EXTRACTION PC /ROTATION VARIMAX /PLOT EIGEN.
Tips: Communality = proportion of a variable's variance explained by the factors.
Use the scree plot to decide how many factors to keep.

PART 4: MEMORY AIDS
- Parametric -> non-parametric swap: t-test -> Mann-Whitney / Wilcoxon;
  ANOVA -> Kruskal-Wallis; repeated ANOVA -> Friedman; Pearson -> Spearman.
- Paired t-test = repeated measures ANOVA with only 2 time points.
- BY in SPSS syntax = grouping / categorical variable.
- WITH in SPSS syntax = predictors / covariates / paired variable.
- Binary DV (0/1) -> think LOGISTIC regression.
- Ordered DV (low/medium/high) -> think ORDERED logistic regression.
- 2 categorical variables -> think CHI-SQUARE.
- Small expected counts (<5) -> FISHER'S EXACT.
- p < .05 -> statistically significant; p >= .05 -> no significant evidence.
- Always check variable type, normality, independence, sample size, assumptions.
- Significant ANOVA -> follow up with post hoc tests.
- Do not write p = .000; write p < .001.
- Do not categorize a continuous variable unnecessarily.

PART 5: FLASHCARDS
Compare means of 2 independent groups, normal data? -> Independent samples t-test
Same, but data not normal (ordinal)? -> Wilcoxon-Mann-Whitney
Compare means of 3+ independent groups, normal data? -> One-way ANOVA
Same, but data not normal? -> Kruskal-Wallis
Before vs after, same people, normal data? -> Paired t-test
Before vs after, not normal? -> Wilcoxon signed-rank
3+ time points, same people, normal data? -> Repeated measures ANOVA
3+ time points, not normal? -> Friedman test
2 categorical variables related? -> Chi-square test of independence
Chi-square with expected count < 5? -> Fisher's exact test
Observed vs expected percentages? -> Chi-square goodness of fit
Proportion vs a fixed value (2 categories)? -> Binomial test
Sample mean vs a fixed value? -> One-sample t-test
Two interval variables linearly related? -> Pearson correlation
Two ordinal variables related? -> Spearman correlation
Predict a number from one variable? -> Simple linear regression
Predict a number from many variables? -> Multiple regression
Predict yes/no from variable(s)? -> Logistic regression
Predict low/medium/high? -> Ordered logistic regression
ANOVA + continuous covariate? -> ANCOVA
2+ factors affecting one outcome? -> Factorial ANOVA
One factor, several outcomes? -> One-way MANOVA
Group two sets of variables relationship? -> Canonical correlation
Reduce many variables to fewer factors? -> Factor analysis
Predict group membership from scores? -> Discriminant analysis
Two matched binary outcomes? -> McNemar test
"""

SYSTEM_PROMPT = """
You are "StatBuddy", a friendly SPSS statistics tutor chatbot. Your specialty is
helping students answer: "What statistical analysis should I use?" using SPSS.

KNOWLEDGE AND SCOPE
- Answer ONLY from the MANUAL provided below.
- If a question is outside statistics / SPSS test selection, politely say that you only
  help with choosing and running statistical tests in SPSS, and invite a stats question.
- If the manual does not cover something, say so honestly and suggest the closest test
  from the manual. Never invent SPSS syntax or numbers.

HOW TO ANSWER
1. Use short sentences and everyday words. Explain any necessary term.
2. For "which test should I use?" identify these three things:
   (a) outcome variable type (interval/normal, ordinal, categorical),
   (b) number of groups/variables,
   (c) independent or paired/repeated data.
   If information is missing, ask ONE short follow-up question before recommending a test.
3. Use this answer format when appropriate:
   ✅ Recommended test: <name>
   🧠 Why: <1-2 simple lines>
   💻 SPSS syntax: <syntax from manual> (and menu path if available)
   📌 How to read the result: explain p < .05 in plain words
   ⚡ Trick/Tip: one memory trick
   🔁 Non-parametric backup: alternative if data is not normal
4. FLASHCARD MODE: if the user types "flashcard", "flashcards", "quiz me" or "test me":
   - Show ONE flashcard question at a time from the manual (Q only, hide the answer).
   - Wait for the user's answer, then say if correct, show the answer, add a one-line tip,
     and ask if they want the next card.
   - Vary topics; do not repeat a card within the same session.
5. If the user types "cheat sheet" or "summary", give a compact decision table.
6. If the user asks for "tips" or "tricks", give 3-5 short memory tricks from the manual.
7. Remind gently that assumptions (normality, independence, expected counts) should be checked.
8. Use friendly emojis sparingly, short bullets, and keep answers under ~200 words unless asked.
9. End each answer with a short follow-up like:
   "Want a flashcard on this, or help with the next step in SPSS?"
10. Be encouraging and never make the user feel silly for asking.

MANUAL:
""" + MANUAL

MODEL = "gemini-2.5-flash"
MAX_HISTORY = 12


def get_client():
    """Create the Gemini client using the key in Streamlit secrets."""
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        st.error(
            "Gemini API key not configured. Add your key to "
            "`.streamlit/secrets.toml` as `GEMINI_API_KEY = \"your-key\"`."
        )
        st.stop()
    return genai.Client(api_key=api_key)


def main():
    st.title("📊 StatBuddy")
    st.caption("Your beginner-friendly SPSS statistical test selector")
    with st.expander("How to use StatBuddy", expanded=False):
        st.markdown(
            "- Ask which statistical test fits your research question.\n"
            "- Type **flashcards** or **quiz me** to practise.\n"
            "- Type **cheat sheet** or **summary** for a compact decision guide.\n"
            "- Type **tips** for memory tricks.\n"
            "- Use **Clear chat** to reset the conversation."
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_error" not in st.session_state:
        st.session_state.api_error = None

    with st.sidebar:
        st.header("Chat controls")
        st.caption(f"Model: `{MODEL}`")
        if st.button("🧹 Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.api_error = None
            st.rerun()
        st.divider()
        st.caption("Conversation memory: last 12 messages (6 Q&A pairs).")
        st.caption("Your Gemini API key is read from `.streamlit/secrets.toml`.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask StatBuddy about your SPSS analysis..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Keep the same rolling history limit as the original chatbot.
        st.session_state.messages = st.session_state.messages[-MAX_HISTORY:]

        with st.chat_message("assistant"):
            with st.spinner("StatBuddy is thinking..."):
                try:
                    client = get_client()
                    gemini_history = [
                        types.Content(
                            role="user" if message["role"] == "user" else "model",
                            parts=[types.Part(text=message["content"])],
                        )
                        for message in st.session_state.messages
                    ]
                    response = client.models.generate_content(
                        model=MODEL,
                        contents=gemini_history,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.3,
                        ),
                    )
                    answer = response.text or (
                        "I couldn't generate a response. Please try again."
                    )
                    st.markdown(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                    st.session_state.messages = st.session_state.messages[-MAX_HISTORY:]
                    st.session_state.api_error = None
                except Exception as exc:
                    # Remove the failed user prompt so it is not sent again as history.
                    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                        st.session_state.messages.pop()
                    st.error(f"Something went wrong: {exc}")
                    st.info("Check your Gemini API key, internet connection, and model access.")


if __name__ == "__main__":
    main()
