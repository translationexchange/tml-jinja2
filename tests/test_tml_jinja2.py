from tml.strings import to_string


def test_dummy(testenv):
    assert to_string("Hello world") == testenv.get_template('dummy.tpl').render(), "pass dummy template"


def test_tr(fake_user, testenv):
    users = {
        'michael': fake_user(**{'gender': 'male', 'first_name': 'Michael', 'last_name': 'Berkovitch'}),
        'anna': fake_user(**{'gender': 'female', 'first_name': 'Anna', 'last_name': 'Tusso'})
    }
    ctx = {'users': users}
    ctx_2 = {'users': [users['michael'], users['anna']]}
    
    def tpl(str, ctx):
        return testenv.get_template(str + ".tpl").render(ctx)

    assert to_string('Hello Michael Berkovitch') == tpl('tr_1', ctx)
    assert to_string('Hello Michael') == tpl('tr_2', ctx)
    assert to_string('Hello Michaell') == tpl('tr_3', ctx)
    assert to_string('Hello Michael') == tpl('tr_4', ctx)
    assert to_string('Hello Michael') == tpl('tr_5', ctx)
    assert to_string('Hello Berkovitch') == tpl('tr_6', ctx)
    assert to_string('Hello Michael') == tpl('tr_7', ctx)
    # list tokens
    assert to_string('Hello Michael and Anna') == tpl('tr_8', ctx_2)
    assert to_string('Hello <b>Michael Berkovitch</b> and <b>Anna Tusso</b>') == tpl('tr_9', ctx_2)
    assert to_string('Hello Michael or Anna') == tpl('tr_10', ctx_2)
    # transform tokens
    assert to_string('This is she') == tpl('tr_11', ctx)
    assert to_string('This is he') == tpl('tr_12', ctx)


def test_trs(fake_user, testenv):
    ctx = {'user': fake_user(gender='female', name='Anna')}

    def tpl(str, ctx):
        return testenv.get_template(str + ".tpl").render(ctx)

    assert to_string('Hello Man') == tpl('trs_1', {})
    assert to_string('Anna') == tpl('trs_2', ctx)
    assert to_string('May') == tpl('trs_3', {})


def test_trs_filter(fake_user, testenv):
    ctx = {'user': fake_user(gender='female', name='Safina')}
    
    def tpl(str, ctx):
        return testenv.get_template(str + ".tpl").render(ctx)

    assert to_string('Safina') == tpl('trs_filter_1', ctx)
    assert to_string('May') == tpl('trs_filter_2', {})


def test_tropts(fake_user, testenv):
    ctx = {'user': fake_user(gender='female', name='Safina'), 'messages': ['', '']}
    
    def tpl(str, ctx):
        return testenv.get_template(str + ".tpl").render(ctx)

    assert to_string('Safina has 2 messages') == tpl('tropts_1', ctx)

def test_tml_inline(testenv):
    def tpl(str, ctx):
        return testenv.get_template(str + ".tpl").render(ctx)

    assert tpl('tml_inline', {}) != ''