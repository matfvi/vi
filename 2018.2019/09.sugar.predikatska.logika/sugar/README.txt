================================================================
README for Sugar version 2

Sugar: A SAT-based Constraint Solver

http://bach.istc.kobe-u.ac.jp/sugar/

================
FEATURES

Sugar can solve a finite linear Constraint Satisfaction Problem (CSP)
or a Constraint Optimization Problem (COP) by encoding it into a
Boolean Satisfiability Testing Problems (SAT) and solving the SAT
problem by using an external SAT solver.

Sugar uses a new SAT-encoding method named "order encoding". In the
order encoding, a comparison x <= a is encoded by a different Boolean
variable for each integer variable x and integer value a. It is an
extension of the encoding method proposed by Crawford and Baker for
the Job-shop scheduling problems to the finite-domain linear CSP
(Constrain Satisfaction Problems).

================
REQUIREMENTS

* Java J2SE 6 or higher

* Perl version 5 or higher

* A SAT Solver

================
INSTALLATION

* Unzip the downloaded zip package.

* Modify the following variable settings of "bin/sugar" to meet your
  execution environment.

  - $java   : Java command path
  - $jar    : Full path of the sugar-v2-1-1.jar file in the same directory
  - $solver : Path of the SAT solver (e.g. MiniSat)
  - $tmp    : Path prefix for temporally created files

================
USAGE

CSPs (Constraint Satisfaction Problems) and COPs (Constraint
Optimization Problems) can be solved by Sugar.

  $ sugar examples/nqueens-8.csp

  $ sugar examples/golombRuler-8.csp

See docs/syntax.html for the syntax of Sugar CSP description.

Sugar can also solve CSPs and MAX-CSPs written in XCSP 2.1 format for
the 2008 CSP solver competition (see http://cpai.ucc.ie/08/).

  $ sugar -competition instance.xml

  $ sugar -competition -max instance.xml

================
DETAILED DESCRIPTION

SAT-encoder and decoder are written in Java.
Perl script "sugar" uses Java programs and SAT solver in the following
way.

* The following temporal files are used.

  - $tmp.csp  : CSP format file
  - $tmp.cnf  : SAT file
  - $tmp.map  : Mapping file
  - $tmp.out  : SAT output file

* XCSP to CSP conversion

  $ java -cp sugar-v2-1-1.jar jp.kobe_u.sugar.XML2CSP file.xml file.csp

* Encoding CSP to SAT

  $ java -jar sugar-v2-1-1.jar -encode file.csp file.cnf file.map

* Solving SAT

  $ minisat file.cnf file.out

* Decoding SAT output

  $ java -jar sugar-v2-1-1.jar [-competition] -decode file.out file.map

================
LIMITATIONS AND KNOWN BUGS

* Multiplications (also divisions and remainders) for two integer
  variables can not be encoded.

* Power functions are not supported.

* CSPs with large domains (e.g. 10,000) will be encoded into very large
  SAT files, and might not be solved by a SAT solver.
       The size of generated SAT file is proportional to the square of
  the domain size in most of the cases.  A very large SAT file (e.g. 
  1GB) might not be solved by most of the SAT solvers.

* If you have enough memory, please try to use jopt1 and jopt2 options.

  $ sugar -jopt1 '-Xmx1500M -Xms1000M -XX:-UseGCOverheadLimit' -jopt2 '-Xmx1000M' input.csp

================
PUBLICATIONS

* Naoyuki Tamura, Akiko Taga, Satoshi Kitagawa, Mutsunori Banbara:
  Compiling Finite Linear CSP into SAT,
  Constraints, Volume 14, Number 2, pp.254--272, June, 2009.
  DOI 10.1007/s10601-008-9061-0 (Open Access, You can freely download the paper)
  http://springer.r.delivery.net/r/r?2.1.Ee.2Tp.1gRdFJ.BxsAdG..N.HAQa.38pS.CLWEcC00

* Naoyuki Tamura, Akiko Taga, Satoshi Kitagawa, Mutsunori Banbara:
  Compiling Finite Linear CSP into SAT,
  in Proceedings of the 12th International Conference on Principles
  and Practice of Constraint Programming (CP 2006),
  pp.590-603, 2006.

* Naoyuki Tamura and Mutsunori Banbara:
  Sugar: A CSP to SAT Translator Based on Order Encoding,
  in Proceedings of the Second International CSP Solver Competition,
  pp.65--69, 2008.

================
LICENSE

This version of the Sugar software is distributed under the BSD
license (http://www.opensource.org/licenses/bsd-license.php).

See LICENSE file for more details.

================
CONTACTS

Naoyuki Tamura, Tomoya Tanjo, and Mutsunori Banbara
Information Science and Technology Center, Kobe University
1-1 Rokkodai, Nada, Kobe 657-8501 Japan
E-mail: tamura @ kobe-u.ac.jp, banbara @ kobe-u.ac.jp

================================================================
