import io

import pytest

from river.time_series import HoltWinters


@pytest.fixture
def printer():
    class Printer:
        def __init__(self):
            self.buffer = io.StringIO()

        def __call__(self, text):
            print(text, file=self.buffer)

        def __repr__(self):
            return self.buffer.getvalue()

    return Printer()


@pytest.fixture
def oil():
    return [
        445.3641,
        453.1950,
        454.409,
        422.3789,
        456.0371,
        440.3866,
        425.1944,
        486.2052,
        500.4291,
        521.2759,
        508.9476,
        488.8889,
        509.8706,
        456.7229,
        473.8166,
        525.9509,
        549.8338,
        542.3405,
    ]


@pytest.fixture
def ausair():
    return [
        17.55340,
        21.86010,
        23.88660,
        26.92930,
        26.88850,
        28.83140,
        30.07510,
        30.95350,
        30.18570,
        31.57970,
        32.57757,
        33.47740,
        39.02158,
        41.38643,
        41.59655,
        44.65732,
        46.95177,
        48.72884,
        51.48843,
        50.02697,
        60.64091,
        63.36031,
        66.35527,
        68.19795,
        68.12324,
        69.77935,
        72.59770,
    ]


@pytest.fixture
def austourists():
    return [
        42.20566,
        24.64917,
        32.66734,
        37.25735,
        45.24246,
        29.35048,
        36.34421,
        41.78208,
        49.27660,
        31.27540,
        37.85063,
        38.83704,
        51.23690,
        31.83855,
        41.32342,
        42.79900,
        55.70836,
        33.40714,
        42.31664,
        45.15712,
        59.57608,
        34.83733,
        44.84168,
        46.97125,
        60.01903,
        38.37118,
        46.97586,
        50.73380,
        61.64687,
        39.29957,
        52.67121,
        54.33232,
        66.83436,
        40.87119,
        51.82854,
        57.49191,
        65.25147,
        43.06121,
        54.76076,
        59.83447,
        73.25703,
        47.69662,
        61.09777,
        66.05576,
    ]


def test_oil(printer, oil):
    """https://otexts.com/fpp2/ses.html#example-oil-production"""

    model = HoltWinters(alpha=0.8339)
    model.level.append(446.5868)
    model._initialized = True

    template = "{:>2d} | {:>8.2f} | {:>8.2f} | {:>8.2f}"
    printer("t  | y        | level    | y_pred")
    printer("-----------------------------------")

    for t, y in enumerate(oil, start=1):
        y_pred = model.forecast(1)[0]
        model.learn_one(y)
        printer(template.format(t, y, model.level[-1], y_pred))

    for h, y_pred in enumerate(model.forecast(5), start=1):
        printer(f"{t + h:>2d} |          |          |   {y_pred:.2f}")

    expected = """
t  | y        | level    | y_pred
-----------------------------------
 1 |   445.36 |   445.57 |   446.59
 2 |   453.19 |   451.93 |   445.57
 3 |   454.41 |   454.00 |   451.93
 4 |   422.38 |   427.63 |   454.00
 5 |   456.04 |   451.32 |   427.63
 6 |   440.39 |   442.20 |   451.32
 7 |   425.19 |   428.02 |   442.20
 8 |   486.21 |   476.54 |   428.02
 9 |   500.43 |   496.46 |   476.54
10 |   521.28 |   517.15 |   496.46
11 |   508.95 |   510.31 |   517.15
12 |   488.89 |   492.45 |   510.31
13 |   509.87 |   506.98 |   492.45
14 |   456.72 |   465.07 |   506.98
15 |   473.82 |   472.36 |   465.07
16 |   525.95 |   517.05 |   472.36
17 |   549.83 |   544.39 |   517.05
18 |   542.34 |   542.68 |   544.39
19 |          |          |   542.68
20 |          |          |   542.68
21 |          |          |   542.68
22 |          |          |   542.68
23 |          |          |   542.68"""

    assert repr(printer).strip() == expected.strip()


def test_ausair(printer, ausair):
    """https://otexts.com/fpp2/holt.html#example-air-passengers"""

    model = HoltWinters(alpha=0.8302, beta=1e-04)
    model.level.append(15.5715)
    model.trend.append(2.1017)
    model._initialized = True

    template = "{:>2d} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f}"
    printer("t  | y        | level    | trend    | y_pred")
    printer("----------------------------------------------")

    for t, y in enumerate(ausair, start=1):
        y_pred = model.forecast(1)[0]
        model.learn_one(y)
        printer(template.format(t, y, model.level[-1], model.trend[-1], y_pred))

    for h, y_pred in enumerate(model.forecast(5), start=1):
        printer(f"{t + h:>2d} |          |          |          |    {y_pred:.2f}")

    expected = """
t  | y        | level    | trend    | y_pred
----------------------------------------------
 1 |    17.55 |    17.57 |     2.10 |    17.67
 2 |    21.86 |    21.49 |     2.10 |    19.68
 3 |    23.89 |    23.84 |     2.10 |    23.59
 4 |    26.93 |    26.76 |     2.10 |    25.94
 5 |    26.89 |    27.22 |     2.10 |    28.86
 6 |    28.83 |    28.92 |     2.10 |    29.33
 7 |    30.08 |    30.24 |     2.10 |    31.02
 8 |    30.95 |    31.19 |     2.10 |    32.34
 9 |    30.19 |    30.71 |     2.10 |    33.29
10 |    31.58 |    31.79 |     2.10 |    32.81
11 |    32.58 |    32.80 |     2.10 |    33.89
12 |    33.48 |    33.72 |     2.10 |    34.90
13 |    39.02 |    38.48 |     2.10 |    35.82
14 |    41.39 |    41.25 |     2.10 |    40.58
15 |    41.60 |    41.89 |     2.10 |    43.35
16 |    44.66 |    44.54 |     2.10 |    44.00
17 |    46.95 |    46.90 |     2.10 |    46.65
18 |    48.73 |    48.78 |     2.10 |    49.00
19 |    51.49 |    51.38 |     2.10 |    50.88
20 |    50.03 |    50.61 |     2.10 |    53.49
21 |    60.64 |    59.30 |     2.10 |    52.72
22 |    63.36 |    63.03 |     2.10 |    61.40
23 |    66.36 |    66.15 |     2.10 |    65.13
24 |    68.20 |    68.21 |     2.10 |    68.25
25 |    68.12 |    68.49 |     2.10 |    70.31
26 |    69.78 |    69.92 |     2.10 |    70.60
27 |    72.60 |    72.50 |     2.10 |    72.02
28 |          |          |          |    74.60
29 |          |          |          |    76.70
30 |          |          |          |    78.80
31 |          |          |          |    80.91
32 |          |          |          |    83.01
"""

    assert repr(printer).strip() == expected.strip()


def test_austourists_additive(printer, austourists):
    """https://otexts.com/fpp2/holt-winters.html#example-international-tourist-visitor-nights-in-australia"""

    model = HoltWinters(alpha=0.3063, beta=1e-04, gamma=0.4263, seasonality=4)
    model.level.append(32.2597)
    model.trend.append(0.7014)
    model.season.extend([9.6962, -9.3132, -1.6935, 1.3106])
    model._initialized = True

    template = "{:>2d} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>11.2f} | {:>8.2f}"
    printer("t  | y        | level    | trend    | seasonality | y_pred")
    printer("------------------------------------------------------------")

    for t, y in enumerate(austourists, start=1):
        y_pred = model.forecast(1)[0]
        model.learn_one(y)
        printer(template.format(t, y, model.level[-1], model.trend[-1], model.season[-1], y_pred))

    for h, y_pred in enumerate(model.forecast(8), start=1):
        printer(f"{t + h:>2d} |          |          |          |             |    {y_pred:.2f}")

    expected = """
t  | y        | level    | trend    | seasonality | y_pred
------------------------------------------------------------
 1 |    42.21 |    32.82 |     0.70 |        9.50 |    42.66
 2 |    24.65 |    33.66 |     0.70 |       -9.13 |    24.21
 3 |    32.67 |    34.36 |     0.70 |       -1.69 |    32.67
 4 |    37.26 |    35.33 |     0.70 |        1.69 |    36.37
 5 |    45.24 |    35.94 |     0.70 |        9.38 |    45.54
 6 |    29.35 |    37.21 |     0.70 |       -8.35 |    27.52
 7 |    36.34 |    37.95 |     0.70 |       -1.64 |    36.21
 8 |    41.78 |    39.09 |     0.70 |        2.30 |    40.34
 9 |    49.28 |    39.83 |     0.70 |        9.42 |    49.17
10 |    31.28 |    40.25 |     0.70 |       -8.73 |    32.18
11 |    37.85 |    40.50 |     0.70 |       -2.26 |    39.31
12 |    38.84 |    39.77 |     0.70 |        0.31 |    43.51
13 |    51.24 |    40.89 |     0.70 |        9.99 |    49.90
14 |    31.84 |    41.28 |     0.70 |       -9.16 |    32.85
15 |    41.32 |    42.47 |     0.70 |       -1.58 |    39.72
16 |    42.80 |    42.96 |     0.70 |        0.02 |    43.48
17 |    55.71 |    44.29 |     0.70 |       10.87 |    53.66
18 |    33.41 |    44.25 |     0.70 |      -10.20 |    35.83
19 |    42.32 |    44.63 |     0.70 |       -2.03 |    43.38
20 |    45.16 |    45.27 |     0.70 |       -0.06 |    45.35
21 |    59.58 |    46.81 |     0.70 |       12.04 |    56.84
22 |    34.84 |    46.75 |     0.70 |      -11.25 |    37.31
23 |    44.84 |    47.27 |     0.70 |       -2.28 |    45.43
24 |    46.97 |    47.69 |     0.70 |       -0.46 |    47.91
25 |    60.02 |    48.26 |     0.70 |       11.86 |    60.42
26 |    38.37 |    49.17 |     0.70 |      -10.97 |    37.71
27 |    46.98 |    49.68 |     0.70 |       -2.54 |    47.59
28 |    50.73 |    50.63 |     0.70 |       -0.12 |    49.92
29 |    61.65 |    50.86 |     0.70 |       11.20 |    63.20
30 |    39.30 |    51.16 |     0.70 |      -11.52 |    40.59
31 |    52.67 |    52.89 |     0.70 |       -1.11 |    49.33
32 |    54.33 |    53.85 |     0.70 |        0.25 |    53.48
33 |    66.83 |    54.88 |     0.70 |       11.66 |    65.76
34 |    40.87 |    54.61 |     0.70 |      -12.88 |    44.07
35 |    51.83 |    54.58 |     0.70 |       -2.12 |    54.20
36 |    57.49 |    55.88 |     0.70 |        1.08 |    55.53
37 |    65.25 |    55.67 |     0.70 |       10.38 |    68.25
38 |    43.06 |    56.24 |     0.70 |      -13.06 |    43.49
39 |    54.76 |    56.92 |     0.70 |       -2.15 |    54.82
40 |    59.83 |    57.97 |     0.70 |        1.56 |    58.71
41 |    73.26 |    59.96 |     0.70 |       12.18 |    69.05
42 |    47.70 |    60.69 |     0.70 |      -13.02 |    47.59
43 |    61.10 |    61.96 |     0.70 |       -1.36 |    59.24
44 |    66.06 |    63.22 |     0.70 |        2.34 |    64.22
45 |          |          |          |             |    76.10
46 |          |          |          |             |    51.60
47 |          |          |          |             |    63.97
48 |          |          |          |             |    68.37
49 |          |          |          |             |    78.90
50 |          |          |          |             |    54.41
51 |          |          |          |             |    66.77
52 |          |          |          |             |    71.18"""

    assert repr(printer).strip() == expected.strip()


def test_austourists_multiplicative(printer, austourists):
    """https://otexts.com/fpp2/holt-winters.html#example-international-tourist-visitor-nights-in-australia"""

    model = HoltWinters(alpha=0.441, beta=0.03, gamma=0.002, seasonality=4, multiplicative=True)
    model.level.append(32.4875)
    model.trend.append(0.6974)
    model.season.extend([1.2442, 0.7704, 0.9618, 1.0237])
    model._initialized = True

    template = "{:>2d} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>11.2f} | {:>8.2f}"
    printer("t  | y        | level    | trend    | seasonality | y_pred")
    printer("------------------------------------------------------------")

    for t, y in enumerate(austourists, start=1):
        y_pred = model.forecast(1)[0]
        model.learn_one(y)
        printer(template.format(t, y, model.level[-1], model.trend[-1], model.season[-1], y_pred))

    for h, y_pred in enumerate(model.forecast(8), start=1):
        printer(f"{t + h:>2d} |          |          |          |             |    {y_pred:.2f}")

    expected = """
t  | y        | level    | trend    | seasonality | y_pred
------------------------------------------------------------
 1 |    42.21 |    33.51 |     0.71 |        1.24 |    41.29
 2 |    24.65 |    33.24 |     0.68 |        0.77 |    26.36
 3 |    32.67 |    33.94 |     0.68 |        0.96 |    32.62
 4 |    37.26 |    35.40 |     0.70 |        1.02 |    35.44
 5 |    45.24 |    36.22 |     0.71 |        1.24 |    44.92
 6 |    29.35 |    37.44 |     0.72 |        0.77 |    28.44
 7 |    36.34 |    38.00 |     0.72 |        0.96 |    36.71
 8 |    41.78 |    39.64 |     0.74 |        1.02 |    39.64
 9 |    49.28 |    40.04 |     0.73 |        1.24 |    50.25
10 |    31.28 |    40.70 |     0.73 |        0.77 |    31.41
11 |    37.85 |    40.51 |     0.70 |        0.96 |    39.84
12 |    38.84 |    39.77 |     0.66 |        1.02 |    42.20
13 |    51.24 |    40.76 |     0.67 |        1.24 |    50.30
14 |    31.84 |    41.39 |     0.67 |        0.77 |    31.91
15 |    41.32 |    42.46 |     0.68 |        0.96 |    40.44
16 |    42.80 |    42.55 |     0.66 |        1.02 |    44.16
17 |    55.71 |    43.90 |     0.68 |        1.24 |    53.77
18 |    33.41 |    44.05 |     0.67 |        0.77 |    34.35
19 |    42.32 |    44.40 |     0.66 |        0.96 |    43.00
20 |    45.16 |    44.64 |     0.65 |        1.02 |    46.13
21 |    59.58 |    46.43 |     0.68 |        1.24 |    56.35
22 |    34.84 |    46.28 |     0.66 |        0.77 |    36.29
23 |    44.84 |    46.80 |     0.65 |        0.96 |    45.14
24 |    46.97 |    46.76 |     0.63 |        1.02 |    48.57
25 |    60.02 |    47.76 |     0.64 |        1.24 |    58.98
26 |    38.37 |    49.03 |     0.66 |        0.77 |    37.28
27 |    46.98 |    49.32 |     0.65 |        0.96 |    47.78
28 |    50.73 |    49.79 |     0.64 |        1.02 |    51.14
29 |    61.65 |    50.04 |     0.63 |        1.24 |    62.77
30 |    39.30 |    50.82 |     0.64 |        0.77 |    39.03
31 |    52.67 |    52.92 |     0.68 |        0.96 |    49.49
32 |    54.33 |    53.37 |     0.67 |        1.02 |    54.86
33 |    66.83 |    53.89 |     0.67 |        1.24 |    67.26
34 |    40.87 |    53.90 |     0.65 |        0.77 |    42.03
35 |    51.83 |    54.26 |     0.64 |        0.96 |    52.46
36 |    57.49 |    55.46 |     0.66 |        1.02 |    56.19
37 |    65.25 |    54.49 |     0.61 |        1.24 |    69.84
38 |    43.06 |    55.46 |     0.62 |        0.77 |    42.44
39 |    54.76 |    56.46 |     0.63 |        0.96 |    53.93
40 |    59.83 |    57.69 |     0.65 |        1.02 |    58.43
41 |    73.26 |    58.57 |     0.66 |        1.24 |    72.59
42 |    47.70 |    60.42 |     0.69 |        0.77 |    45.62
43 |    61.10 |    62.17 |     0.72 |        0.96 |    58.77
44 |    66.06 |    63.62 |     0.74 |        1.02 |    64.38
45 |          |          |          |             |    80.09
46 |          |          |          |             |    50.16
47 |          |          |          |             |    63.34
48 |          |          |          |             |    68.18
49 |          |          |          |             |    83.80
50 |          |          |          |             |    52.45
51 |          |          |          |             |    66.21
52 |          |          |          |             |    71.23"""

    assert repr(printer).strip() == expected.strip()
