/*
  Copyright 2002 Raph Levien

  This program is free software; you can redistribute it and/or modify
  it under the terms of version 2 of the GNU General Public License as
  published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
  USA
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <glib.h>
#include "net_flow.h"
#include "page_rank.h"

int
get_graph_line (char *line, char **pfrom, char **pto, char **pcolor)
{
  char *from;
  char *to;
  char *color;
  int i;

  if (line[0] == ' ' && line[1] == ' ' && line[2] == ' ')
    {
      i = 3;
      from = line + i;
      while (line[i] && line[i] != ' ') i++;
      if (!memcmp(line + i, " -> ", 4))
	{
	  line[i] = 0;
	  i += 4;
	  to = line + i;
	  while (line[i] && line[i] != ' ') i++;
	  line[i] = 0;
	  *pfrom = from;
	  *pto = to;
	  *pcolor = NULL;
	  return 1;
	}
    }
  return 0;
}

typedef struct PrSort {
  int n;
  double rank;
} PrSortEl;

static int
pr_sort_cmp (const void *a, const void *b)
{
  double r1 = ((const PrSortEl *)a)->rank;
  double r2 = ((const PrSortEl *)b)->rank;

  if (r1 < r2) return 1;
  else if (r1 > r2) return -1;
  else return 0;
}

void
print_page_rank (PageRank *pr, double *r)
{
  int n_nodes = pr->n_nodes;
  int i;
  PrSortEl *perm = g_new (PrSortEl, n_nodes);

  for (i = 0; i < n_nodes; i++)
    {
      perm[i].n = i;
      perm[i].rank = r[i];
    }
  qsort (perm, n_nodes, sizeof(PrSortEl), pr_sort_cmp);
  for (i = 0; i < n_nodes; i++)
    printf ("%4d %20s: %g\n", i,
	    page_rank_node_name (pr, perm[i].n), perm[i].rank);
  g_free (perm);
}

int
run_page_rank (FILE *f, int argc, char **argv)
{
  char line[128];
  PageRank *pr = page_rank_new ();
  int seed;
  double *r;

  seed = page_rank_find_node (pr, "-");
  page_rank_add_edge (pr, "-", "rillian");

  for (;;)
    {
      char *from;
      char *to;
      char *color;

      if (fgets (line, sizeof(line), f) == NULL)
	break;
      if (get_graph_line (line, &from, &to, &color))
	page_rank_add_edge (pr, from, to);
    }
  r = page_rank_compute (pr, seed, 0.15);
#if 0
  print_page_rank (pr, r);
#endif
  g_free (r);
  return 0;
}

int
run_net_flow (FILE *f, int argc, char **argv)
{
  char line[128];
  NetFlow *nf = net_flow_new ();
  int caps[] = { 1900, 300, 100, 30, 10, 3, 1, 0 };
  int seed;

  seed = net_flow_find_node (nf, "-");
  net_flow_add_edge (nf, "-", "raph");
  net_flow_add_edge (nf, "-", "alan");
  net_flow_add_edge (nf, "-", "wsanchez");
  net_flow_add_edge (nf, "-", "rasmus");

  for (;;)
    {
      char *from;
      char *to;
      char *color;

      if (fgets (line, sizeof(line), f) == NULL)
	break;
      if (get_graph_line (line, &from, &to, &color))
	net_flow_add_edge (nf, from, to);
    }
  net_flow_max_flow (nf, seed, caps, sizeof(caps)/sizeof(caps[0]));
  return 0;
}

int
main (int argc, char **argv)
{
  FILE *f = stdin;

  return run_page_rank (f, argc, argv);
}
