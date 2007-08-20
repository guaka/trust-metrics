#!/usr/bin/env python

__author__ = 'Vincent Kraeutler';

# from http://kraeutler.net/vincent/essays/google%20page%20rank%20in%20python
# Vincent gives permission to use this code under the terms of the GPL

from numpy import *

def pageRankGenerator(
	At = [array((), int32)], 
	numLinks = array((), int32),  
	ln = array((), int32),
	alpha = 0.85, 
	convergence = 0.01, 
	checkSteps = 10
	):
	"""
	Compute an approximate page rank vector of N pages to within some convergence factor.
	@param At a sparse square matrix with N rows. At[ii] contains the indices of pages jj linking to ii.
	@param numLinks iNumLinks[ii] is the number of links going out from ii. 
	@param ln contains the indices of pages without links
	@param alpha a value between 0 and 1. Determines the relative importance of "stochastic" links.
	@param convergence a relative convergence criterion. smaller means better, but more expensive.
	@param checkSteps check for convergence after so many steps
	"""

	# the number of "pages"
	N = len(At)

	# the number of "pages without links"
	M = ln.shape[0]

	# initialize: single-precision should be good enough
	iNew = ones((N,), float32) / N
	iOld = ones((N,), float32) / N

	done = False
	while not done:

		# normalize every now and then for numerical stability
		iNew /= sum(iNew)
	
		for step in range(checkSteps):

			# swap arrays
			iOld, iNew = iNew, iOld

			# an element in the 1 x I vector. 
			# all elements are identical.
			oneIv = (1 - alpha) * sum(iOld) / N

			# an element of the A x I vector.
			# all elements are identical.
			oneAv = 0.0
			if M > 0:
				oneAv = alpha * sum(iOld.take(ln, axis = 0)) * M / N
		
			# the elements of the H x I multiplication
			ii = 0 
			while ii < N:
				page = At[ii]
				h = 0
				if page.shape[0]:
					h = alpha * dot(
						iOld.take(page, axis = 0),
						1. / numLinks.take(page, axis = 0)
						)
				iNew[ii] = h + oneAv + oneIv
				ii += 1
		
		diff = iNew - iOld
		done = (sqrt(dot(diff, diff)) / N < convergence)
		
		yield iNew


def transposeLinkMatrix(
	outGoingLinks = [[]]
	):
	"""
	Transpose the link matrix. The link matrix contains the pages each page points to.
	But what we want is to know which pages point to a given page, while retaining information
	about how many links each page contains (so store that in a separate array),
	as well as which pages contain no links at all (leaf nodes).

	@param outGoingLinks outGoingLinks[ii] contains the indices of pages pointed to by page ii
	@return a tuple of (incomingLinks, numOutGoingLinks, leafNodes)
	"""

	nPages = len(outGoingLinks)
	# incomingLinks[ii] will contain the indices jj of the pages linking to page ii
	incomingLinks = [[] for ii in range(nPages)]
	# the number of links in each page
	numLinks = zeros(nPages, int32)
	# the indices of the leaf nodes
	leafNodes = []

	for ii in range(nPages):
		if len(outGoingLinks[ii]) == 0:
			leafNodes.append(ii)
		else:
			numLinks[ii] = len(outGoingLinks[ii])
			# transpose the link matrix
			for jj in outGoingLinks[ii]:
				incomingLinks[jj].append(ii)
	
	incomingLinks = [array(ii) for ii in incomingLinks]
	numLinks = array(numLinks)
	leafNodes = array(leafNodes)

	return incomingLinks, numLinks, leafNodes
				

def pageRank(
	linkMatrix = [[]],
        alpha = 0.85, 
	convergence = 0.01, 
	checkSteps = 10
        ):
	"""
	Convenience wrap for the link matrix transpose and the generator.

	@see pageRankGenerator for parameter description
	"""
	incomingLinks, numLinks, leafNodes = transposeLinkMatrix(linkMatrix)

        for gr in pageRankGenerator(incomingLinks, numLinks, leafNodes, alpha = alpha, convergence = convergence, checkSteps = checkSteps):
                final = gr

        return final
