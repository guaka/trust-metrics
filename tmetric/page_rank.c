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

/*
  This file implements the PageRank algorithm as described in:

  @techreport{ page98pagerank,
    author = "Lawrence Page and Sergey Brin and Rajeev Motwani and Terry Winograd",
    title = "The {P}age{R}ank Citation Ranking: Bringing Order to the Web",
    institution = "Stanford University",
    year = "1998",
    url = "citeseer.nj.nec.com/page98pagerank.html"
  }

  While this implementation is released under GPL for research purposes,
  it is entirely plausible that the authors and/or Google have patents
  that cover the work. Please do not use for non-research purposes
  without checking with a competent lawyer first.
*/


#include <glib.h>
#include <math.h>
#include "page_rank.h"

PageRank *
page_rank_new (void)
{
  PageRank *result = g_new (PageRank, 1);

  result->n_nodes = 0;
  result->n_nodes_max = 16;
  result->n_succs = g_new (int, result->n_nodes_max);
  result->n_succs_max = g_new (int, result->n_nodes_max);
  result->succs = g_new (int *, result->n_nodes_max);
  result->capacity = NULL;
  result->node_id = g_hash_table_new (g_str_hash, g_str_equal);
  result->names = NULL;

  return result;
}

static void
page_rank_free_helper (gpointer key, gpointer value, gpointer user_data)
{
  g_free (key);
}

void
page_rank_free (PageRank *self)
{
  int i;

  g_hash_table_foreach (self->node_id, page_rank_free_helper, NULL);
  g_hash_table_destroy (self->node_id);


  for (i = 0; i < self->n_nodes; i++)
    g_free (self->succs[i]);
  g_free (self->n_succs);
  g_free (self->n_succs_max);
  g_free (self->succs);
  if (self->capacity != NULL)
    g_free (self->capacity);
  if (self->names != NULL)
    g_free (self->names);

  g_free (self);
}

gint
page_rank_find_node (PageRank *self, const char *name)
{
  gpointer resultptr;

  if (g_hash_table_lookup_extended (self->node_id,
				    name,
				    NULL,
				    &resultptr))
    return GPOINTER_TO_INT(resultptr);
  resultptr = GINT_TO_POINTER (self->n_nodes);
  g_hash_table_insert (self->node_id, g_strdup (name), resultptr);

  if (self->n_nodes == self->n_nodes_max)
    {
      self->n_nodes_max <<= 1;
      self->n_succs = g_realloc (self->n_succs,
				 sizeof(int) * self->n_nodes_max);
      self->n_succs_max = g_realloc (self->n_succs_max,
				     sizeof(int) * self->n_nodes_max);
      self->succs = g_realloc (self->succs, sizeof(int *) * self->n_nodes_max);
      if (self->capacity != NULL)
	self->capacity = g_realloc (self->capacity,
				    sizeof(int) * self->n_nodes_max);
    }
  self->n_succs[self->n_nodes] = 0;
  self->n_succs_max[self->n_nodes] = 16;
  self->succs[self->n_nodes] = g_new (int, self->n_succs_max[self->n_nodes]);

  return self->n_nodes++;
}

static void
page_rank_node_name_helper (gpointer key, gpointer value, gpointer user_data)
{
  PageRank *self = user_data;

  self->names[GPOINTER_TO_INT (value)] = key;
}

/**
 * page_rank_node_name: Find name of numbered node.
 * @self: The #PageRank context.
 * @node: The node number.
 *
 * Finds the name of the numbered node. Note: this is intended primarily
 * for debugging and is certainly not coded for speed.
 *
 * Return value: The name of the node, or NULL if not found.
 **/
char *
page_rank_node_name (PageRank *self, int node)
{

  /* todo: doesn't gracefully handle new names after first call of this
     method. */
  if (!self->names)
    {
      self->names = g_new (char *, self->n_nodes);
      g_hash_table_foreach (self->node_id, page_rank_node_name_helper, self);
    }

  return self->names[node];
}

void
page_rank_add_edge (PageRank *self, const char *src, const char *dst)
{
  gint src_id;
  gint dst_id;

  src_id = page_rank_find_node (self, src);
  dst_id = page_rank_find_node (self, dst);
  if (src_id == dst_id)
    /* skip self-edges */
    return;
  if (self->n_succs[src_id] == self->n_succs_max[src_id])
    {
      self->n_succs_max[src_id] <<= 1;
      self->succs[src_id] = g_realloc (self->succs[src_id],
				       self->n_succs_max[src_id] *
				       sizeof(int));
    }
  self->succs[src_id][self->n_succs[src_id]++] = dst_id;
}

static double
page_rank_iter (PageRank *self,
		double *r, double *r_new, double *e)
{
  int n_nodes = self->n_nodes;
  int i, j, src;
  double sum_r_new;
  double r_scale, delta;

  for (i = 0; i < n_nodes; i++)
    r_new[i] = 0;
  sum_r_new = 0;

  /* step r forward */
  for (src = 0; src < n_nodes; src++)
    {
      int n_succ = self->n_succs[src];
      int *succ = self->succs[src];

      if (n_succ == 0)
	continue;

      sum_r_new += r[src];
      delta = r[src] / n_succ;

      for (j = 0; j < n_succ; j++)
	r_new[succ[j]] += delta;
    }

  r_scale = 1 / sum_r_new;
  delta = 0;
  /* do normalize and e */
  for (i = 0; i < n_nodes; i++)
    {
      double new_r = r_new[i] * r_scale + e[i];
      delta += fabs (new_r - r[i]);
      r[i] = new_r;
    }
  return delta;
}

/**
 * page_rank_compute: Compute PageRank.
 * @self: The graph.
 * @damping: Damping factor, equivalent to ||E||_1.
 *
 * This implementation basically has E(seed) = damping, and E otherwise
 * zero.
 *
 * Return value: a newly allocated array with the result.
 **/
double *
page_rank_compute (PageRank *self, gint seed, double damping)
{
  int n_nodes = self->n_nodes;
  double *r = g_new (double, n_nodes);
  double *r_new = g_new (double, n_nodes);
  double *e = g_new (double, n_nodes);
  double delta;
  int i;

  for (i = 0; i < self->n_nodes; i++)
    e[i] = 0;

  e[seed] = damping;
  memcpy (r, e, sizeof(double) * n_nodes);

  for (i = 0; i < 50; i++)
    {
      delta = page_rank_iter (self, r, r_new, e);
      printf ("delta = %f\n", delta);
    }

  g_free (r_new);
  g_free (e);
  return r;
}
