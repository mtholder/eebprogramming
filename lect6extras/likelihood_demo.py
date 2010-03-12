#!/usr/bin/env python
import sys, math, os, random
from PyQt4 import QtGui, QtCore
pattern_count_filename = os.environ.get("PATTERN_COUNT_FILE")

def parse_counts_from_fn(pattern_count_filename):
    print "Going to try reading", pattern_count_filename, "..."
    inp = open(pattern_count_filename, 'rU')
    pcd = [float(i.strip()) for i in inp if i.strip()]
    assert len(pcd) > 7
    for i in pcd:
        assert i >= 0.0
    return pcd


if pattern_count_filename:
    try:
        pattern_count_data = parse_counts_from_fn(pattern_count_filename)
    except:
        sys.exit("Expecting %s to be a file of pattern counts (one-per line)." % pattern_count_filename)
else:
    pattern_count_data = [0]*8
class BranchEnum:
    A, B, INTERNAL, C, D = 0, 1, 2, 3, 4
    names = ["A", "B", "Internal", "C", "D"]
# ratios of dimensions for 45 degree lines
HYP_OVER_HORIZ = math.sqrt(2)
HORIZ_OVER_HYP = 1/HYP_OVER_HORIZ
HYP_OVER_VERT = math.sqrt(2)
VERT_OVER_HYP = 1/HYP_OVER_VERT
TOL = 0.000001
NUM_STATES = 2
MAX_BRANCH_LEN = (NUM_STATES - 1.0)/NUM_STATES
AS_CENTRAL_WIDGET = False
if AS_CENTRAL_WIDGET:
    TreeWindowBase = QtGui.QWorkspace
else:
    TreeWindowBase = QtGui.QDialog
class TopologyEnum:
    AB, AC, AD = 0, 1, 2
    names = ["AB | CD", "AC | BD", "AD | BC"]
    colors = [QtCore.Qt.red, QtCore.Qt.blue, QtCore.Qt.green]
    txt_fmt = ['<font color="red">%s</font>', '<font color="blue">%s</font>', '<font color="green">%s</font>']
    best_txt_fmt = ['<font color="red"><u>%s</u></font>', '<font color="blue"><u>%s</u></font>', '<font color="green"><u>%s</u></font>']
SHOW_DATA_BARS = [True, True, True, True]
def randomly_choose_indices(p, n):
    """Treats `p` as a list of category probabilities.  Returns as list of `n`
    indices that were randomly drawn from this discrete probability distribution.
    Does not verify that sum(p) == 1.0.  All rounding error is "given" to the
    list category.
    """
    last_ind = len(p) - 1
    c = [0]*len(p)
    for i in xrange(n):
        u = random.random()
        ind = 0
        while ind < last_ind:
            u -= p[ind]
            if u < 0.0:
                break
            ind += 1
        c[ind] = c[ind] + 1
    return c
class MultiBarWidget(QtGui.QWidget):
    def __init__(self, parent):
        self.h = []
        QtGui.QWidget.__init__(self, parent)
        self.max_dim = 300
        self.max_prob = 1.0
        self.px_per_unit_prob = self.max_dim/self.max_prob
        self.bar_dim = 10
        self.bar_skip = 0
        self.setMinimumHeight(4.5*(self.bar_dim+ self.bar_skip))
        self.setMinimumWidth(self.max_dim)
    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)
        colors = [QtCore.Qt.black, QtCore.Qt.red, QtCore.Qt.blue, QtCore.Qt.green, ]
        y = 0
        for n, b in enumerate(self.h):
            if SHOW_DATA_BARS[n]:
                w = b*self.px_per_unit_prob
                r = QtCore.QRect(0, y, w, self.bar_dim)
                curr_color = colors[n]
                paint.fillRect(r, curr_color)
            #print 0, y, w, self.bar_dim
            y += self.bar_dim + self.bar_skip
        paint.end()
class LnLWorkspace(TreeWindowBase):
    """Internally the tree calculations are done as if we have a AB|CD tree.
    Then patterns and branch lengths are swapped into the correct order.
    """
    def __init__(self, prob_sources, parent=None):
        QtGui.QWidget.__init__(self, parent)
        assert(len(prob_sources) == 3)
        self.prob_sources = prob_sources
        abp, acp, adp = [i.calc_pat_probs() for i in self.prob_sources]
        self.setWindowTitle("Data and Likelihoods")
        gridLayout = QtGui.QGridLayout()
        dheader = QtGui.QLabel("Data (counts)")
        gridLayout.addWidget(dheader, 0, 0)
        tax_labels = QtGui.QLabel("A B C D")
        gridLayout.addWidget(tax_labels, 0, 1)
        self.showDataChkBox = QtGui.QCheckBox("Data")
        self.showAB = QtGui.QCheckBox("AB")
        self.showAC = QtGui.QCheckBox("AC")
        self.showAD = QtGui.QCheckBox("AD")
        self.showBarsBoxes = [self.showDataChkBox, self.showAB, self.showAC, self.showAD]
        for el in self.showBarsBoxes:
            el.setChecked(True)
            self.connect(el,  QtCore.SIGNAL('stateChanged(int)'), self.show_bars_changed)
        gridLayout.addWidget(self.showDataChkBox, 0, 2)
        gridLayout.addWidget(self.showAB, 0, 3)
        gridLayout.addWidget(self.showAC, 0, 4)
        gridLayout.addWidget(self.showAD, 0, 5)
        patternCountValidator = QtGui.QDoubleValidator(self)
        patternCountValidator.setBottom(0.0)
        self.data_labels = []
        self.data_counts = []
        self.plot_widget_list = []
        for i in range(8):
            bits = bin(8 + i)[3:]
            lab = QtGui.QLabel("0 %s" % " ".join(bits))
            vlab = QtGui.QLineEdit()
            vlab.setMaximumWidth(100)
            vlab.setText("0")
            vlab.setValidator(patternCountValidator)
            self.data_labels.append(lab)
            self.data_counts.append(vlab)
            plot_widget = MultiBarWidget(self)
            plot_widget.h = [0.0, abp[i], acp[i], adp[i]]
            self.plot_widget_list.append(plot_widget)
            gridLayout.addWidget(vlab, 1 + i, 0)
            gridLayout.addWidget(lab, 1 + i, 1)
            gridLayout.addWidget(plot_widget, 1 + i, 2, 1, 3)
        for el in self.data_counts:
            self.connect(el,  QtCore.SIGNAL('textChanged(QString)'), self.counts_changed)
        w = QtGui.QLabel('ln(Likelihood)')
        gridLayout.addWidget(w, 9, 0, 1, 2)
        w = QtGui.QLabel('Parsimony score')
        gridLayout.addWidget(w, 10, 0, 1, 2)
        # font for the text boxes for the lnL
        self.notBestFont = QtGui.QFont()
        self.bestFont = QtGui.QFont()
        self.bestFont.setUnderline(True)
        self.lnL_labels = [QtGui.QLabel(''), QtGui.QLabel(''), QtGui.QLabel('')]
        for n, el in enumerate(self.lnL_labels):
            gridLayout.addWidget(el, 9, 2 + n)
        self.pars_labels = [QtGui.QLabel(''), QtGui.QLabel(''), QtGui.QLabel('')]
        for n, el in enumerate(self.pars_labels):
            gridLayout.addWidget(el, 10, 2 + n)
        self.setLayout(gridLayout)
        self.resize(570, 500)
    def show_bars_changed(self):
        for n, el in enumerate(self.showBarsBoxes):
            if el.isChecked():
                SHOW_DATA_BARS[n] = True
            else:
                SHOW_DATA_BARS[n] = False
        self.repaint()
    def counts_changed(self):
        abp, acp, adp = [i.calc_pat_probs() for i in self.prob_sources]
        c = [float(i.text() or 0) for i in self.data_counts]
        #print c
        t = sum(c)
        have_data = True
        if t == 0.0:
            t = 1.0
            have_data = False
        for n, el in enumerate(c):
            self.plot_widget_list[n].h = [el/t, abp[n], acp[n], adp[n]]
            self.plot_widget_list[n].repaint()
        if have_data:
            lnL_values = self.calc_ln_L()
            pars_scores = self.calc_pars_scores()
            #print pars_scores
            highest_index = lnL_values.index(max(lnL_values))
            most_pars_index = pars_scores.index(min(pars_scores))
            as_str = ["%6.2f" % i for i in lnL_values]
            for n, el in enumerate(self.lnL_labels):
                if n == highest_index:
                    el.setFont(self.bestFont)
                else:
                    el.setFont(self.notBestFont)
                fmt_str = TopologyEnum.txt_fmt[n]
                txt = TopologyEnum.txt_fmt[n] % as_str[n]
                el.setText(txt)
                el.show()
            as_str = ["%6.2f" % i for i in pars_scores]
            for n, el in enumerate(self.pars_labels):
                if n == most_pars_index:
                    el.setFont(self.bestFont)
                else:
                    el.setFont(self.notBestFont)
                fmt_str = TopologyEnum.txt_fmt[n]
                txt = TopologyEnum.txt_fmt[n] % as_str[n]
                el.setText(txt)
                el.show()
        self.repaint()
    def probs_changed(self):
        self.counts_changed()
        self.repaint()
    def get_counts(self):
        c = []
        for i in self.data_counts:
            try:
                x = float(i.text())
            except:
                x = 0.0
            c.append(x)
        return c
    def calc_pars_scores(self):
        c = self.get_counts()
        non_const = sum(c[1:])
        homoplasy_ab = c[5] + c[6]
        homoplasy_ac = c[3] + c[6]
        homoplasy_ad = c[3] + c[5]
        return [non_const + homoplasy_ab, non_const + homoplasy_ac, non_const + homoplasy_ad]
    def calc_ln_L(self):
        c = self.get_counts()
        freqs = [i.calc_pat_probs() for i in self.prob_sources]
        return [self.calc_ln_L_from_counts(c, f) for f in freqs]
    def calc_ln_L_from_counts(self, counts, freqs):
        sum = 0.0
        for n, c in enumerate(counts):
            if c > 0:
                f = freqs[n]
                try:
                    char_ln_l = c*math.log(f)
                except ValueError:
                    return float('-inf')
                sum += char_ln_l
        return sum
    def set_counts(self, pattern_count_data):
        for n, x in enumerate(pattern_count_data):
            try:
                self.data_counts[n].setText(str(int(x)))
            except:
                self.data_counts[n].setText(str(x))
            if n == 7:
                break
        self.repaint()
def crop_branch_len(x):
    if x < 0.0:
        return 0.0
    if x > MAX_BRANCH_LEN:
        return MAX_BRANCH_LEN
    return x
class TreeWorkspace(TreeWindowBase):
    """Internally the tree calculations are done as if we have a AB|CD tree.
    Then patterns and branch lengths are swapped into the correct order.
    """
    def __init__(self, parent=None, topology=TopologyEnum.AB):
        QtGui.QWidget.__init__(self, parent)
        self.topology = topology
        self.lnLPanel = None
        self.setWindowTitle(TopologyEnum.names[self.topology])
        gridLayout = QtGui.QGridLayout()
        self.labels = []
        self.spinboxes = []
        self.opt_buttons = []
        for i in range(5):
            lab = QtGui.QLabel("length of '%s'" % BranchEnum.names[i])
            sb = QtGui.QDoubleSpinBox()
            sb.setRange(0.0, MAX_BRANCH_LEN)
            sb.setDecimals(4)
            sb.setSingleStep(0.005)
            sb.setValue(0.05)
            gridLayout.addWidget(lab, i, 2)
            gridLayout.addWidget(sb, i, 1)
            self.labels.append(lab)
            self.spinboxes.append(sb)
            self.connect(sb,  QtCore.SIGNAL('valueChanged(double)'), self.brlen_changed)
            opt = QtGui.QPushButton("Optimize")
            self.opt_buttons.append(opt)
            gridLayout.addWidget(opt, i, 0)
            self.connect(opt,  QtCore.SIGNAL('clicked()'), getattr(self, "opt_" + BranchEnum.names[i]))
        opt = QtGui.QPushButton("Optimize all")
        self.opt_buttons.append(opt)
        gridLayout.addWidget(opt, 5, 0)
        self.connect(opt,  QtCore.SIGNAL('clicked()'), self.opt_all)
        pat_pr = self.calc_pat_probs()
        self.pr_labels = []
        self.pr_values = []
        for i in range(8):
            bits = bin(8 + i)[3:]
            lab = QtGui.QLabel("Pr(0%s) =" % bits)
            vlab = QtGui.QLabel("%0.5f" % pat_pr[i])
            self.pr_labels.append(lab)
            self.pr_values.append(vlab)
            #gridLayout.addWidget(lab, i, 3)
            #gridLayout.addWidget(vlab, i, 4)
            #gridLayout.setRowStretch(i, 1)
        #gridLayout.setColumnStretch(0, .5)
        #gridLayout.setColumnStretch(1, .5)
        self.treeCanvas = QtGui.QFrame()
        gridLayout.setRowMinimumHeight(6, 250)
        gridLayout.addWidget(self.treeCanvas, 6, 0, 1, 5)
        self.treePaintX, self.treePaintY = (50, 300)
        self.treePaintScaler = 300
        self.treePen = QtGui.QPen(TopologyEnum.colors[self.topology], 2, QtCore.Qt.SolidLine)
        sim = QtGui.QPushButton("Simulate...")
        self.load_data_button = QtGui.QPushButton("Load Data")
        gridLayout.addWidget(sim, 9, 0)
        gridLayout.addWidget(self.load_data_button, 10, 0)
        self.num_chars_edit = QtGui.QLineEdit()
        num_char_validator = QtGui.QIntValidator(self)
        num_char_validator.setBottom(0)
        self.num_chars_edit.setText("500")
        self.num_chars_edit.setValidator(num_char_validator)
        gridLayout.addWidget(self.num_chars_edit, 9, 1)
        lab = QtGui.QLabel("... characters")
        gridLayout.addWidget(lab, 9, 2)
        self.connect(sim,  QtCore.SIGNAL('clicked()'), self.simulate)
        self.connect(self.load_data_button,  QtCore.SIGNAL('clicked()'), self.load_data)
        self.setLayout(gridLayout)
        self.resize(570, 400)
    def simulate(self):
        if not self.lnLPanel:
            return
        try:
            t = self.num_chars_edit.text()
            n = int(t)
        except:
            raise
        p = self.calc_pat_probs()
        c = randomly_choose_indices(p, n)
        print "simulated counts = ", c
        self.lnLPanel.set_counts(c)

    def load_data(self):
        if not self.lnLPanel:
            return
        load_data_filedialog = QtGui.QFileDialog(self)
        #sys.stderr.write("\n".join(dir(load_data_filedialog)))
        if load_data_filedialog.exec_():
            f = load_data_filedialog.selectedFiles()
            if f:
                pattern_count_filename= f[0]
                try:
                    c = parse_counts_from_fn(pattern_count_filename)
                    self.lnLPanel.set_counts(c)
                except:
                    sys.stderr.write("Error reading data from %s" % pattern_count_filename)


    def do_opt(self, value_holder, curr_step=0.04):
        calc = self.lnLPanel
        if not calc:
            return
        data = calc.get_counts()
        if sum(data) == 0.0:
            return
        curr_pat_p = self.calc_pat_probs()
        curr_v = value_holder.value()
        curr_lnL = calc.calc_ln_L_from_counts(data, curr_pat_p)
        best_v, best_lnL = curr_v, curr_lnL
        lower_lnL = None
        lower_v = curr_v
        higher_lnL = None
        higher_v = curr_v
        while True:
            if lower_lnL is not None and lower_lnL - TOL > curr_lnL:
                curr_v, curr_lnL = lower_v, lower_lnL
                value_holder.setValue(curr_v)
            elif higher_lnL is not None and  higher_lnL - TOL > curr_lnL:
                curr_v, curr_lnL = higher_v, higher_lnL
            else:
                if (higher_lnL is not None) and (lower_lnL is not None):
                    if (abs(lower_lnL - curr_lnL) < TOL) and (abs(lower_lnL - curr_lnL) < TOL):
                        value_holder.setValue(curr_v)
                        self.repaint()
                        return curr_v, curr_lnL
                    if curr_lnL == float('-inf'):
                        return curr_v, curr_lnL
                curr_step /= 2
            best_v, best_lnL = curr_v, curr_lnL
            lower_v = crop_branch_len(curr_v - curr_step)
            value_holder.setValue(lower_v)
            p = self.calc_pat_probs()
            lower_lnL = calc.calc_ln_L_from_counts(data, p)
            self.repaint()
            higher_v = crop_branch_len(curr_v + curr_step)
            value_holder.setValue(higher_v)
            p = self.calc_pat_probs()
            higher_lnL = calc.calc_ln_L_from_counts(data, p)
            self.repaint()
            #print lower_v, "=>", lower_lnL
            #print curr_v, "=>", curr_lnL
            #print higher_v, "=>", higher_lnL
    def opt_all(self):
        curr_step = 0.04
        v, prev_lnl = self.opt_A(curr_step=curr_step)
        same_score_count = 0
        while True:
            self.opt_Internal(curr_step=curr_step)
            self.opt_A(curr_step=curr_step)
            self.opt_B(curr_step=curr_step)
            self.opt_C(curr_step=curr_step)
            v, curr_lnl = self.opt_D(curr_step=curr_step)
            #print "prev_lnl,  curr_lnl = ", prev_lnl,  curr_lnl
            if abs(prev_lnl - curr_lnl) < TOL:
                same_score_count += 1
            else:
                same_score_count = 0
            if same_score_count > 1:
                return
            prev_lnl = curr_lnl
            curr_step /= 10
    def opt_A(self,curr_step=0.04):
        return self.do_opt(self.spinboxes[BranchEnum.A], curr_step=curr_step)
    def opt_B(self,curr_step=0.04):
        return self.do_opt(self.spinboxes[BranchEnum.B], curr_step=curr_step)
    def opt_Internal(self,curr_step=0.04):
        return self.do_opt(self.spinboxes[BranchEnum.INTERNAL], curr_step=curr_step)
    def opt_C(self,curr_step=0.04):
        return self.do_opt(self.spinboxes[BranchEnum.C], curr_step=curr_step)
    def opt_D(self,curr_step=0.04):
        return self.do_opt(self.spinboxes[BranchEnum.D], curr_step=curr_step)
    def get_br_lens(self):
        return [i.value() for i in self.spinboxes]
    def get_funky_ordered_br_lens(self):
        if self.topology == TopologyEnum.AB:
            return self.get_br_lens()
        a_ch, b_ch, int_ch, c_ch, d_ch = self.get_br_lens()
        if self.topology == TopologyEnum.AC:
            b_ch, c_ch = c_ch, b_ch
        else:
            b_ch, c_ch, d_ch = d_ch, b_ch, c_ch
        return a_ch, b_ch, int_ch, c_ch, d_ch
    def calc_pat_p_scores(self):
        """Pattern parsimony scores returned in order:
        A  00000000
        B  00001111
        C  00110011
        D  01010101
        """
        if self.topology == TopologyEnum.AB:
            return (0, 1, 1, 1, 1, 2, 2, 1)
        elif self.topology == TopologyEnum.AC:
            return (0, 1, 1, 2, 1, 1, 2, 1)
        return (0, 1, 1, 2, 1, 2, 1, 1)
    def calc_pat_probs(self):
        """Pattern likelihoods returned in order (assumes CFN with A=0),
        A  00000000
        B  00001111
        C  00110011
        D  01010101
        """
        b = self.get_funky_ordered_br_lens()
        a_ch, b_ch, int_ch, c_ch, d_ch = b
        a_no_ch, b_no_ch, int_no_ch, c_no_ch, d_no_ch = [1.0 - i for i in b]
        # print "b = ", b
        # ab anc
        ab0, ab1= a_no_ch, a_ch
        # ab anc and b
        b0ab0 = ab0*b_no_ch
        b1ab0 = ab0*b_ch
        b0ab1 = ab1*b_ch
        b1ab1 = ab1*b_no_ch
        # print b0ab0, b1ab0, b0ab1, b1ab1
        # ab anc, b and cd anc
        b0ab0cd0 = b0ab0*int_no_ch
        b0ab0cd1 = b0ab0*int_ch
        b1ab0cd0 = b1ab0*int_no_ch
        b1ab0cd1 = b1ab0*int_ch
        b0ab1cd0 = b0ab1*int_ch
        b0ab1cd1 = b0ab1*int_no_ch
        b1ab1cd0 = b1ab1*int_ch
        b1ab1cd1 = b1ab1*int_no_ch
        # b and cd anc
        b0cd0 = b0ab0cd0 + b0ab1cd0
        b1cd0 = b1ab0cd0 + b1ab1cd0
        b0cd1 = b0ab0cd1 + b0ab1cd1
        b1cd1 = b1ab0cd1 + b1ab1cd1
        # b, c and cd anc
        b0cd0c0 = b0cd0*c_no_ch
        b0cd0c1 = b0cd0*c_ch
        b1cd0c0 = b1cd0*c_no_ch
        b1cd0c1 = b1cd0*c_ch
        b0cd1c0 = b0cd1*c_ch
        b0cd1c1 = b0cd1*c_no_ch
        b1cd1c0 = b1cd1*c_ch
        b1cd1c1 = b1cd1*c_no_ch
        # b, c, d and cd anc
        b0cd0c0d0 = b0cd0c0*d_no_ch
        b0cd0c0d1 = b0cd0c0*d_ch
        b0cd0c1d0 = b0cd0c1*d_no_ch
        b0cd0c1d1 = b0cd0c1*d_ch
        b1cd0c0d0 = b1cd0c0*d_no_ch
        b1cd0c0d1 = b1cd0c0*d_ch
        b1cd0c1d0 = b1cd0c1*d_no_ch
        b1cd0c1d1 = b1cd0c1*d_ch
        b0cd1c0d0 = b0cd1c0*d_ch
        b0cd1c0d1 = b0cd1c0*d_no_ch
        b0cd1c1d0 = b0cd1c1*d_ch
        b0cd1c1d1 = b0cd1c1*d_no_ch
        b1cd1c0d0 = b1cd1c0*d_ch
        b1cd1c0d1 = b1cd1c0*d_no_ch
        b1cd1c1d0 = b1cd1c1*d_ch
        b1cd1c1d1 = b1cd1c1*d_no_ch
        # b, c, d
        b0c0d0 = b0cd0c0d0 + b0cd1c0d0
        b0c0d1 = b0cd0c0d1 + b0cd1c0d1
        b0c1d0 = b0cd0c1d0 + b0cd1c1d0
        b0c1d1 = b0cd0c1d1 + b0cd1c1d1
        b1c0d0 = b1cd0c0d0 + b1cd1c0d0
        b1c0d1 = b1cd0c0d1 + b1cd1c0d1
        b1c1d0 = b1cd0c1d0 + b1cd1c1d0
        b1c1d1 = b1cd0c1d1 + b1cd1c1d1
        # swap elements
        if self.topology == TopologyEnum.AC:
            b0c0d0 , b0c0d1 , b0c1d0 , b0c1d1 , b1c0d0 , b1c0d1 , b1c1d0 , b1c1d1 = (b0c0d0 , b0c0d1 , b1c0d0 , b1c0d1 , b0c1d0 , b0c1d1 , b1c1d0 , b1c1d1)
        elif self.topology == TopologyEnum.AD:
            b0c0d0 , b0c0d1 , b0c1d0 , b0c1d1 , b1c0d0 , b1c0d1 , b1c1d0 , b1c1d1 = (b0c0d0 , b1c0d0 , b0c0d1 , b1c0d1 , b0c1d0 , b1c1d0 , b0c1d1 , b1c1d1)
        # return with d = ones bit, c = 2's bit, d = 4's bit
        return (b0c0d0 , b0c0d1 , b0c1d0 , b0c1d1 , b1c0d0 , b1c0d1 , b1c1d0 , b1c1d1)
    def brlen_changed(self):
        self.repaint()
        if self.lnLPanel:
            self.lnLPanel.probs_changed()
    def refresh_pat_prob_GUI(self):
        pat_pr = self.calc_pat_probs()
        for i, item in enumerate(self.pr_values):
            t = "%0.5f" % pat_pr[i]
            item.setText(t)
            # print i, t
    def paintEvent(self, event):
        self.refresh_pat_prob_GUI()
        paint = QtGui.QPainter()
        paint.begin(self)
        scaler = self.treePaintScaler
        abAncX = (self.treePaintX + MAX_BRANCH_LEN*scaler*HORIZ_OVER_HYP)
        abAncY = (self.treePaintY+ MAX_BRANCH_LEN*scaler*VERT_OVER_HYP)
        a_len, b_len, int_len, c_len, d_len = self.get_funky_ordered_br_lens()
        cdAncX = abAncX + scaler*int_len
        cdAncY = abAncY
        aX = abAncX - scaler*HORIZ_OVER_HYP*a_len
        aY = abAncY - scaler*VERT_OVER_HYP*a_len
        bX = abAncX - scaler*HORIZ_OVER_HYP*b_len
        bY = abAncY + scaler*VERT_OVER_HYP*b_len
        cX = cdAncX + scaler*HORIZ_OVER_HYP*c_len
        cY = cdAncY - scaler*VERT_OVER_HYP*c_len
        dX = cdAncX + scaler*HORIZ_OVER_HYP*d_len
        dY = cdAncY + scaler*VERT_OVER_HYP*d_len
        font_x_offset = 10
        font_y_offset = 5
        if self.topology == TopologyEnum.AB:
            b_text, c_text, d_text = "B", "C", "D"
        elif self.topology == TopologyEnum.AC:
            b_text, c_text, d_text = "C", "B", "D"
        else:
            b_text, c_text, d_text = "D", "B", "C"
        paint.setPen(self.treePen)
        paint.drawLine(abAncX, abAncY, cdAncX, cdAncY)
        paint.drawLine(abAncX, abAncY, aX, aY)
        paint.drawText(aX - font_x_offset, aY + font_y_offset, "A")
        paint.drawLine(abAncX, abAncY, bX, bY)
        paint.drawText(bX - font_x_offset, bY+ font_y_offset, b_text)
        paint.drawLine(cdAncX, cdAncY, cX, cY)
        paint.drawText(cX+4, cY + font_y_offset, c_text)
        paint.drawLine(cdAncX, cdAncY, dX, dY)
        paint.drawText(dX+4, dY+ font_y_offset, d_text)
        paint.end()
class LikelihoodApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('tree likelihood visualizer')
        sb = self.statusBar()
        self.abTree = TreeWorkspace(topology=TopologyEnum.AB)
        if AS_CENTRAL_WIDGET:
            self.setCentralWidget = self.abTree
            self.resize(self.abTree.width(), self.abTree.height() + sb.height())
        else:
            self.acTree = TreeWorkspace(topology=TopologyEnum.AC)
            self.adTree = TreeWorkspace(topology=TopologyEnum.AD)
            self.lnL = LnLWorkspace(prob_sources=[self.abTree, self.acTree, self.adTree])
            self.abTree.lnLPanel = self.lnL
            self.acTree.lnLPanel = self.lnL
            self.adTree.lnLPanel = self.lnL
            self.lnL.move(0,0)
            self.abTree.move(500,20)
            self.acTree.move(520,40)
            self.adTree.move(530,50)
    def show(self):
        if not AS_CENTRAL_WIDGET:
            self.acTree.show()
            self.abTree.show()
            self.adTree.show()
            self.lnL.show()
        QtGui.QMainWindow.show(self)
app = QtGui.QApplication(sys.argv)
qb = LikelihoodApp()
qb.show()
qb.lnL.set_counts(pattern_count_data)
sys.exit(app.exec_())
