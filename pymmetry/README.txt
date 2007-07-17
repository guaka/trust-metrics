
TITLE INFORMATION: Pymmetry - Python Trust Metrics 
AUTHOR INFORMATION: Luke Kenneth Casson Leighton 
DATE INFORMATION: Mon Mar 26 00:00:59 BST 2001 

Pymmetry has a Maximum Flow (Ford-Faulkersson) implementation
at its heart, which is used to provide an easy means to evaluate
Trust Metric Certifications, in python.

Trust Metric Evaluations, essentially, are Cascading (or,
Hierarchical) Access Control Lists.  Pymmetry provides an
easy way to integrate Trust Metrics into any project.

Practical applications for Trust Metrics include Domain Name
Registration protection, Web-site Forum / content access
rights and privileges evaluation, and any other potentially
hostile environment in which it is necessary to distinguish
trusted from untrusted entities, taking into consideration
the opinions of entities in the field.

1: History

The original code for Pymmetry
(http://pymmetry.sourceforge.net)
has gone via
http://virgule.sourceforge.net
from mod_virgule, by Raph Levien <raph@acm.org>.  Raph studied
Trust Metrics, and wrote mod_virgule - a community site
forum engine - as a social experiment which has proved highly
successful and effective at its job.  Namely, it promotes and
protects a site's purpose from unsolicited interference by
empowering the users, in a hostile environment [e.g. the
internet], to select those people that they trust within
their community to remain honour-bound to the charter of
the site they are using, or risk the wrath of their peers -
ultimately expressed by the revokation of the Certifications
their peers gave them, with the inherent loss of access rights
such revokation implies.

Raph's original Network flow simulation code was written
in Java.  For mod_virgule's purposes, he rewrote it in c.
Pymmetry is a python implementation, which is considerably
more flexible, cleaner and easier to understand than c.

The original purpose of Raph's Trust Metric code was to fulfil
a similar aim to that of Keynote.  Namely, that in a large
hostile environment, you have to know who to trust (and the
example in his paper was the issue of Domain Name registration).
When you have a chain (or web) of trust, you have to be able
to evaluate that chain, and be as certain as possible that
the web has not been compromised, in order to make decisions.

Keynote focusses, effectively, on "a means to securely evaluate
Digitally-signed Logical Expressions".  Whilst Raph's work is
known, because of http://advogato.org,
for focussing on the web of trust and its evaluation, Raph's
original paper does cover "Logical Expressions" as well,
of which - it turns out - Keynote is a superset implementation.

There has been much discussion recently about Trust Metrics -
most notably on http://advogato.org,
the original Open Source Advocacy site, set up by Raph.
It is hoped that Pymmetry will add fuel to the flames :)

2: HOWTO

Each of the files in the Pymmetry project have a demonstration
test.  tm_calc.py contains details on how to use the TrustMetric
class, and file_certs.py is example code that creates some
user profiles and certifications in text files.  The rest of
this document describes the Pymmetry classes and how to use
them effectively.

3: Certification base classes

certs.py provides the base-level classes for Certification
manipulation.  It provides the functions that must be
implemented to access Certifications by type, including the
levels (see class CertInfo), and it provides the means by
which users can add and remove Certifications of specific
types (again, see class CertInfo) on other users (see class
Certifications).

Certifications work in conjunction with Profiles, implemented
in profile.py.

file_certs.py provides example file-based
Certification classes: see below.

4: Base classes to evaluate Trust Metrics

profile.py provides the means to access user profiles,
including user's Certifications of other users (see
certs.py) .

The TrustMetric class must be given the means to obtain user
profiles and certifications in order to perform an evaluation,
and this is done through a class derived from Profile.
For example, one such Profile access mechanism may be to read
user profiles using HTTP on remote sites, thereby extending
Trust Metric evaluations into the realm of Distributed webs
(along with all the associated problems that entails :)

file_certs.py provides example file-based
Profile classes: see below.

5: File-based Trust Metric Profiles

File-based Profiles on which certifications (also file-based) can
be stored and retrieved for evaluation by Trust Metrics.  This code is
intended as an example / demonstration.

6: Network Maximum Flow Graph

This is an almost line-for-line translation of Raph's original
c code, net_flow.c.  It implements the standard Ford-Faulkersson
Maximum Flow algorithm, on an arbitrarily-linked weighted graph.

Example usage:
	f = NetFlow()
	f.netflow_add_edge(item1, item2)
	f.netflow_add_edge(class1, item2)
	f.netflow_add_edge(..., ...)
	...

	capacity_list = [NNNN, NNN, NN, NN, N, N, N]
	mf1 = f.netflow_max_flow_extract(supersink, capacity_list)
	mf2 = f.netflow_max_flow_extract(supersink2, capacity_list)
	...

Note: items (nodes) are stored in a dictionary.  Therefore,
[just in case you're new to python] you can therefore evaluate
anything.  names, strings, unicode, numbers, tuples, complex
numbers, classes - whatever you like.

TODO: look at Raph's paper, get the formula for the recommended
capacity calculations (which are based on the number of nodes)
and use that as the default for if capacity_list is None

7: Trust Metric Calculation

TrustMetric is the main class that actually
performs a Trust Metric evaluation.  It is based on
tm_calc.c from http://virgule.sourceforge.net which in turn is based on
the original code tmetric.c, by Raph Levien, in mod_virgule.

Example usage:
	p = Profiles(ProfileClass, CertificationsClass)
	c = CertInfoClass()
	t = TrustMetric(c, p)
	r = t.tmetric_calc(certification_type_name, [optional seed list])

The variables are explained as follows:

o p - an instance of a user-profile holder, where:

	o 	ProfileClass (must be derived from Profile)
		is the class responsible for obtaining
		user-profiles, on-demand
	o 	CertificationsClass (must be derived from
		Certifications) is the class responsible for
		obtaining user's certifications of each other,
		on-demand.

o c - an instance of the Certification Information class
	(which must be derived from CertInfo)
o t - an instance of the Trust Metric Evaluation class,
	on which tmetric_calc can be called.

	o 	the certification_type_name must be recognised
		by c, and if you want any results back, the
		users must have certified each other under
		that certification type!
	o 	the optional seed list can over-ride the default
		seed list for the certification type, if required.

o r - a dictionary where:

	o 	the keys are the names of the users
	o 	the values are the level at which each user
		is certified, relative to the input seed(s)
		on the requested evaluation.

Exactly what you do with those results is entirely up
to you.  Here are some uses to which Trust Metrics have
been put:

o 
	advogato.org, skolos.org, jabber.org, ghostview.org
	and badvogato.org use them to let the users themselves
	ascertain who fulfils the criteria associated with the
	site, with a view to allowing them to post articles
	on the front page.
o 
	virgule.sourceforge.net's example site-code takes this
	a stage further, including a newsfeed which requires
	slightly higher certification to post to than articles,
	and has "Interest" certification type which can be used
	for tagging and search capabilities.

	It also "reverses" the Trust Metric's grammatical
	syntax on Projects ("user" is "lead developer" for
	"project" instead of "user" certifies "project" as
	"lead developer" which just doesn't make sense :),
	Allowing people to certify that they are working
	for a person or a project (instead of the project or
	person working for them).  Evaluation of a Project's
	"Developers" metric then cascades a list of developers,
	depending on who is working for who _and_ what.

	This "reversing" is the reason why tmetric_type
	is loaded from the CertType class instance - see
	tmetric_run.

One minor practical difference from Raph's original
tmetric.c (that likewise is carried over from tm_calc.c),
is the concept of "default" certification levels (see
CertInfo.cert_level_default).  The application of this is that
if a user is not certified by _anyone_, they are automatically
certified at the "default" level [whether the Trust Metric
evaluation has enough capacity to _give_ them this level is
another matter entirely].  see tmetric_stage1.

For example, an "Interest" Certification could have levels
"Not Interesting", "Ambivalent" and "Intriguing", with a
default level of "Ambivalent".

Another minor practical difference is the concept of "minimum
level", which in Raph's original tmetric.c is hard-coded to
CERT_LEVEL_NONE.  Imagine that you have several Certification
levels, and yet you use only the top few levels for access
control purposes - _at the present time_.

Performing Maximum Flow calculations is expensive (25,000
nodes with an average of four links per node, in net_flow.py,
on a PIII/800, takes 25 seconds and 1k per node, to evaluate).
So, a "minimum level" concept was added.  No user will receive
a Certification at _below_ this level.

NOTE: if the default level is below or at the minimum level,
and a user receives a Certification from another user at BELOW
OR AT the default level, then that user will NOT be included
in the response from tmetric_calc.

This is intentional.  if a little cryptic.  hmmm... :)

8: Conclusion

There is much scope for the use of Trust Metrics.

Just PLEASE don't use them for "rankings" or "ratings"
of people on a front page.  This is asking for trouble.
If you must "rate" something, then rate what people do,
not who they are.

THINK.	Ratings of people will list the top-rated people on the
site on the front page.  Therefore, clickety-click busy people
will clickety-click certify those people more than others,
which at best turns your entire site into a back-scratching
(or back-stabbing) self-gratification exercise.  "Wow, I Got
More Certs Than You: I'm On The Front Page".  Do you really
want your site to generate a Black Market in Certification
Trading, for the purposes of Ego-Bolstering?

Alternative suggestion: create an "Interest" Certification,
then customise the front page with links to all cascading
"Interest"ing articles, projects, people and anything else
that the user has Certified as "Interest"ing, by performing an
"Interest" tmetric_calc with the viewer as the primary seed.

Combining two Trust Metric calculations becomes even
more powerful: it takes on useful search-engine capabilities,
Imagine that you can search for Open Source Articles certified
by one person that another respected Open Source Developer has
certified as "Interest"ing.  Perform a Trust Metric evaluation
on the "Open Source Advocate" Certification type with the first
person as the seed, perform a second Trust Metric evaluation
on "Interests" with the second person as the seed, and list any
Articles that are common to both evaluations, sorted first by
"Open Source" and second by "Interest" Certification types.

There are some quite serious social responsibilites associated
with the uses of Trust Metrics: it's not just about
programming.  THINK ABOUT IT.
