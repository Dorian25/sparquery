# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:53:31 2019

@author: Dorian
"""
from nltk.tree import Tree
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame
import os.path
import csv

dict_rules = {
	'( SBARQ ( WHNP/WHADVP/WHADJP:qtype_t ) ( SQ:sq_t ) )' : {
	
		'( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) )' : { 
		
			'( SQ ( VP ( ADVP:prop-o ) ) ( VBZ ) ( VP:suject-o ) )' : '1.1.1',
			'( SQ ( VBD:action-o ) ( NP:subj_t ) ( VP:prop-o ) )' : {
				"( NP ( NP:subject-o ) ( VP:prop-o ) )": '1.2.1',
				"( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) )": '1.2.2',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '1.2.3',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '1.2.4',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '1.2.5',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '1.2.6',
				"( NP:subject-o )": '1.2.7'
			},
			'( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP:subj_t ) ) )' : {
				"( NP ( NP:subject-o ) ( VP:prop-o ) )": '1.3.1',
				"( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) )": '1.3.2',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '1.3.3',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '1.3.4',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '1.3.5',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '1.3.6',
				"( NP:subject-o )": '1.3.7'
			},
			'( SQ ( VBZ:action-o ) ( NP:subj_t ) ( VP:prop-o ) )': {
				"( NP ( NP:subject-o ) ( VP:prop-o ) )": '1.4.1',
				"( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) )": '1.4.2',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '1.4.3',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '1.4.4',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '1.4.5',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '1.4.6',
				"( NP:subject-o )": '1.4.7'
			},
			'( SQ ( VBZ/VBD/VBP:action-o ) ( NP:subj_t ) )': {
				"( NP ( NP:subject-o ) ( VP:prop-o ) )": '1.5.1',
				"( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) )": '1.5.2',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '1.5.3',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '1.5.4',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '1.5.5',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '1.5.6',
				"( NP:subject-o )": '1.5.7'
			}
		},
		
		'( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) )' : {
			'( SQ ( VP ( ADVP:prop-o ) ) ( VBZ ) ( VP:suject-o ) )' : '2.1.1',
			'( SQ ( VBD:action-o ) ( NP:subj_t ) ( VP:prop-o ) )' : {
				"( NP ( NP:subject-o ) ( VP:prop-o ) )": '2.2.1',
				"( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) )": '2.2.2',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '2.2.3',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '2.2.4',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '2.2.5',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '2.2.6',
				"( NP:subject-o )": '2.2.7'
			},
			'( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP:subj_t ) ) )' : {
				"( NP ( NP:subject-o ) ( VP:prop-o ) )": '2.3.1',
				"( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) )": '2.3.2',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '2.3.3',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '2.3.4',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '2.3.5',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '2.3.6',
				"( NP:subject-o )": '2.3.7'
			},
			'( SQ ( VBZ:action-o ) ( NP:subj_t ) ( VP:prop-o ) )': {
				"( NP ( NP:subject-o ) ( VP:prop-o ) )": '2.4.1',
				"( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) )": '2.4.2',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '2.4.3',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '2.4.4',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '2.4.5',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '2.4.6',
				"( NP:subject-o )": '2.4.7'
			},
			'( SQ ( VBZ/VBD/VBP:action-o ) ( NP:subj_t ) )': {
				"( NP ( NP:subject-o ) ( VP:prop-o ) )": '2.5.1',
				"( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) )": '2.5.2',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '2.5.3',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '2.5.4',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '2.5.5',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '2.5.6',
				"( NP:subject-o )": '2.5.7'			
			}
		},
		
		'( WHNP/WHADVP:qtype-o )' : {
			'( SQ ( VP ( ADVP:prop-o ) ) ( VBZ ) ( VP:suject-o ) )' : '3.1.1',
			'( SQ ( VBD:action-o ) ( NP:subj_t ) ( VP:prop-o ) )' : {
				"( NP ( NP:subject-o ) ( VP:prop-o ) )": '3.2.1',
				"( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) )": '3.2.2',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '3.2.3',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '3.2.4',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '3.2.5',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '3.2.6',
				"( NP:subject-o )": '3.2.7'
			},
			'( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP:subj_t ) ) )' : {
				"( NP ( NP:subject-o ) ( VP:prop-o ) )": '3.3.1',
				"( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) )": '3.3.2',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '3.3.3',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '3.3.4',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '3.3.5',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '3.3.6',
				"( NP:subject-o )": '3.3.7'
			},
			'( SQ ( VBZ:action-o ) ( NP:subj_t ) ( VP:prop-o ) )': {
				"( NP ( NP:subject-o ) ( VP:prop-o ) )": '3.4.1',
				"( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) )": '3.4.2',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '3.4.3',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '3.4.4',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '3.4.5',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '3.4.6',
				"( NP:subject-o )": '3.4.7'
			},
			'( SQ ( VBZ/VBD/VBP:action-o ) ( NP:subj_t ) )': {
				"( NP ( NP:subject-o ) ( VP:prop-o ) )": '3.5.1',
				"( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) )": '3.5.2',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '3.5.3',
				"( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '3.5.4',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ )": '3.5.5',
				"( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) )": '3.5.6',
				"( NP:subject-o )": '3.5.7'			
			}
		}
	},
	'( SBARQ ( WHNP ( WHNP ( WHADJP:qtype-o ) ( NNS:inst-O ) ) ( PP:prop_match_t ) ) )' : '4.1.1' ,
    '( SBARQ ( WHNP:qtype-o=who ) ( SQ:sq_t ) )' : {
        '( SQ ( VBD/VBZ ) ( NP ( NP:inst-O ) ( PP:prop_match_t ) ) )': '5.1.1'
    },
    '( SBARQ ( WHNP ( WHADJP/WDT/WHNP:qtype-o ) ( NNS/NN/NP:inst-O ) ) ( SQ:sq_t ) )' : {
        '( SQ ( VBP ) ( NP ( EX=there ) ) )' : '6.1.1',
        '( SQ ( VP ( VP:prop_match_t ) ( CC ) ( VP:prop_match2_t ) ) )' : '6.1.2',
        '( SQ ( VP:prop_match_t ) )' : '6.1.3',
        '( SQ:prop_match_t )' : '6.1.4',
	},
    #yes/no
    '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ( PP ( NP ( DT ) ( NN/NNS/NNP/NNPS ) ) ( PP ( IN ) ( NP:subject2-o ( NN/NNS/NNP/NNPS ) ) ) ) )' : '7.1.1',
    '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ( ADJP ( JJ:prop-o ) ) )' : '7.1.2',
    '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NNP/NNS/NN/NNPS ) ( NNP/NNS/NN/NNPS ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP:subject2-o ( NNP/NNS/NN/NNPS ) ) ) ) )' : '7.1.3',
    '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NNP/NNS/NN/NNPS ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP:subject2-o ( NNP/NNS/NN/NNPS ) ( NNP/NNS/NN/NNPS ) ) ) ) )' : '7.1.4',
    '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP:subject2-o ( DT ) ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ) ) )' : '7.1.5',
    '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NNP/NNS/NN/NNPS ) ( NNP/NNS/NN/NNPS ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP:subject2-o ( NNP/NNS/NN/NNPS ) ( NNP/NNS/NN/NNPS ) ) ) ) )' : '7.1.6',
    '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NNP ) ( NNP ) ) ( NP ( DT ) ( NN:subject2-o ) ) )' : '7.1.7',
    '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NN/NNS/NNP/NNPS ) ) ( VP ( VBZ/VBD/VBP/VB/VBN ) ( PP ( IN ) ( NP:subject2-o ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ) ) )' : '7.1.8',
    '( SQ ( VBZ/VBD/VBP/VBN/VB ) ( NP ( NN/NNS/NNP/NNPS:subject-o ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP ( NN/NNS/NNP/NNPS:subject2-o ) ) ) ) )' : '7.1.9',
    '( SQ ( VBZ/VBD/VBP/VBN/VB ) ( NP ( NN/NNS/NNP/NNPS:subject-o ) ) ( ADJP ( JJR:prop-o ) ( PP ( IN ) ( NP ( NN/NNS/NNP/NNPS:subject2-o ) ) ) ) )' : '7.1.10',
    '( SQ ( VBZ/VBD/VBP/VBN/VB ) ( NP ( EX ) ) ( NP ( NP:subject-o ( DT ) ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ( VP ( VBZ/VBD/VBP/VBN/VB ) ( NP:subject2-o ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ) ) )' : '7.1.11',
    #order
    '( SQ ( VP ( VB/VBZ/VBN/VBP/VBG ) ( NP ( PRP ) ) ( NP ( NP ( DT ) ( NN/NNS/NNP/NNPS:prop-o ) ) ( PP ( IN ) ( NP ( NN/NNS/NNP/NNPS:subject-o ) ) ) ) ) )' : '8.1.1',
    '( SQ ( VP ( VB/VBZ/VBN/VBP/VBG ) ( NP ( PRP ) ) ( NP ( PDT ) ( DT ) ( NN/NNS/NNP/NNPS:subject-o ) ) ) )' : '8.1.2',
    '( SQ ( VP ( VB/VBZ/VBN/VBP/VBG ) ( NP:subject-o ( DT ) ( JJ ) ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ) )' : '8.1.3',
    '( SQ ( VP ( VB/VBZ/VBN/VBP/VBG ) ( NP ( NP ( NN/NNS/NNP/NNPS ) ) ( VP ( VB/VBZ/VBN/VBP/VBG:prop-o ) ( PP ( IN ) ( NP:subject2-o ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ) ) ) ) )' : '8.1.4'

}


all_rules = {#qtype_t.sq_t.subj_t 
     '1.1.1': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VP ( ADVP:prop-o ) ) ( VBZ ) ( VP:suject-o ) ) )',
     
     '1.2.1': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ) ( VP:prop-o ) ) ( VP:prop-o ) ) )',
     '1.2.2': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBD:action-o ) ( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) ) ( VP:prop-o ) ) )',
     '1.2.3': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ( VP:prop-o ) ) )',
     '1.2.4': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ( VP:prop-o ) ) )',
     '1.2.5': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ( VP:prop-o ) ) )',
     '1.2.6': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ( VP:prop-o ) ) )',
     '1.2.7': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBD:action-o ) ( NP:subject-o ) ( VP:prop-o ) ) )',
     
     '1.3.1': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ) ( VP:prop-o ) ) ) ) )',
     '1.3.2': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) ) ) ) )',
     '1.3.3': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ) ) )',
     '1.3.4': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ) ) )',
     '1.3.5': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ) ) )',
     '1.3.6': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ) ) )',
     '1.3.7': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP:subject-o ) ) ) )',
     
     '1.4.1': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ) ( VP:prop-o ) ) ( VP:prop-o ) ) )',
     '1.4.2': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ:action-o ) ( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) ) ( VP:prop-o ) ) )',
     '1.4.3': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ( VP:prop-o ) ) )',
     '1.4.4': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ( VP:prop-o ) ) )',
     '1.4.5': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ( VP:prop-o ) ) )',
     '1.4.6': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ( VP:prop-o ) ) )',
     '1.4.7': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ:action-o ) ( NP:subject-o ) ( VP:prop-o ) ) )',
     
     '1.5.1': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ) ( VP:prop-o ) ) ) )',
     '1.5.2': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) ) ) )',
     '1.5.3': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ) )',
     '1.5.4': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ) )',
     '1.5.5': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ) )',
     '1.5.6': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ) )',
     '1.5.7': '( SBARQ ( WHNP ( WDT:qtype-o=what ) ( NN:prop3-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP:subject-o ) ) )',
     
     
     '2.1.1': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VP ( ADVP:prop-o ) ) ( VBZ ) ( VP:suject-o ) ) )',
     
     '2.2.1': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ) ( VP:prop-o ) ) ( VP:prop-o ) ) )',
     '2.2.2': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBD:action-o ) ( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) ) ( VP:prop-o ) ) )',
     '2.2.3': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ( VP:prop-o ) ) )',
     '2.2.4': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ( VP:prop-o ) ) )',
     '2.2.5': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ( VP:prop-o ) ) )',
     '2.2.6': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ( VP:prop-o ) ) )',
     '2.2.7': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBD:action-o ) ( NP:subject-o ) ( VP:prop-o ) ) )',
     
     '2.3.1': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ) ( VP:prop-o ) ) ) ) )',
     '2.3.2': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) ) ) ) )',
     '2.3.3': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ) ) )',
     '2.3.4': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ) ) )',
     '2.3.5': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ) ) )',
     '2.3.6': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ) ) )',
     '2.3.7': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP:subject-o ) ) ) )',
     
     '2.4.1': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ) ( VP:prop-o ) ) ( VP:prop-o ) ) )',
     '2.4.2': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ:action-o ) ( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) ) ( VP:prop-o ) ) )',
     '2.4.3': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ( VP:prop-o ) ) )',
     '2.4.4': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ( VP:prop-o ) ) )',
     '2.4.5': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ( VP:prop-o ) ) )',
     '2.4.6': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ( VP:prop-o ) ) )',
     '2.4.7': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ:action-o ) ( NP:subject-o ) ( VP:prop-o ) ) )',
     
     '2.5.1': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ) ( VP:prop-o ) ) ) )',
     '2.5.2': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) ) ) )',
     '2.5.3': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ) )',
     '2.5.4': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ) )',
     '2.5.5': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ) )',
     '2.5.6': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ) )',
     '2.5.7': '( SBARQ ( WHADJP ( WRB:qtype-o ) ( JJ:jj-o ) ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP:subject-o ) ) )',
     
     
     '3.1.1': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VP ( ADVP:prop-o ) ) ( VBZ ) ( VP:suject-o ) ) )',
     
     '3.2.1': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ) ( VP:prop-o ) ) ( VP:prop-o ) ) )',
     '3.2.2': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBD:action-o ) ( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) ) ( VP:prop-o ) ) )',
     '3.2.3': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ( VP:prop-o ) ) )',
     '3.2.4': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ( VP:prop-o ) ) )',
     '3.2.5': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ( VP:prop-o ) ) )',
     '3.2.6': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBD:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ( VP:prop-o ) ) )',
     '3.2.7': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBD:action-o ) ( NP:subject-o ) ( VP:prop-o ) ) )',
     
     '3.3.1': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ) ( VP:prop-o ) ) ) ) )',
     '3.3.2': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) ) ) ) )',
     '3.3.3': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ) ) )',
     '3.3.4': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ) ) )',
     '3.3.5': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ) ) )',
     '3.3.6': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ) ) )',
     '3.3.7': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VP ( VBZ/VBD/VBP:action-o ) ( NP:subject-o ) ) ) )',
     
     '3.4.1': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ) ( VP:prop-o ) ) ( VP:prop-o ) ) )',
     '3.4.2': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ:action-o ) ( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) ) ( VP:prop-o ) ) )',
     '3.4.3': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ( VP:prop-o ) ) )',
     '3.4.4': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ( VP:prop-o ) ) )',
     '3.4.5': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ( VP:prop-o ) ) )',
     '3.4.6': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ( VP:prop-o ) ) )',
     '3.4.7': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ:action-o ) ( NP:subject-o ) ( VP:prop-o ) ) )',
     
     '3.5.1': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ) ( VP:prop-o ) ) ) )',
     '3.5.2': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:prop-o ) ( PP ( IN ) ( NP:subject-o ) ) ) ) )',
     '3.5.3': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ) )',
     '3.5.4': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ) )',
     '3.5.5': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/NNS:prop-o ) $ ) ) )',
     '3.5.6': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP ( NP:subject-o ( NNP ) ( NNP ) ( POS ) ) ( NN/JJ:prop-o ) ( NN/NNS:prop2-o ) ) ) )',
     '3.5.7': '( SBARQ ( WHNP/WHADVP:qtype-o ) ( SQ ( VBZ/VBD/VBP:action-o ) ( NP:subject-o ) ) )',
     
     #find entity rules
     '4.1.1' : '( SBARQ ( WHNP ( WHNP ( WHADJP:qtype-o ) ( NNS:inst-O ) ) ( PP:prop_match_t ) ) )',
     '5.1.1' : '( SBARQ ( WHNP:qtype-o=who ) ( SQ ( VBD/VBZ ) ( NP ( NP:inst-O ) ( PP:prop_match_t ) ) ) )',
     '6.1.1' : '( SBARQ ( WHNP ( WHADJP/WDT/WHNP:qtype-o ) ( NNS/NN/NP:inst-O ) ) ( SQ ( VBP ) ( NP ( EX=there ) ) ) )',
     '6.1.2' : '( SBARQ ( WHNP ( WHADJP/WDT/WHNP:qtype-o ) ( NNS/NN/NP:inst-O ) ) ( SQ ( VP ( VP:prop_match_t ) ( CC ) ( VP:prop_match2_t ) ) ) )',
     '6.1.3' : '( SBARQ ( WHNP ( WHADJP/WDT/WHNP:qtype-o ) ( NNS/NN/NP:inst-O ) ) ( SQ ( VP:prop_match_t ) ) )',
     '6.1.4' : '( SBARQ ( WHNP ( WHADJP/WDT/WHNP:qtype-o ) ( NNS/NN/NP:inst-O ) ) ( SQ:prop_match_t ) )',

     #yes/no question
     '7.1.1' : '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ( PP ( NP ( DT ) ( NN/NNS/NNP/NNPS ) ) ( PP ( IN ) ( NP:subject2-o ( NN/NNS/NNP/NNPS ) ) ) ) )',
     '7.1.2' : '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ( ADJP ( JJ:prop-o ) ) )',
     '7.1.3' : '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NNP/NNS/NN/NNPS ) ( NNP/NNS/NN/NNPS ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP:subject2-o ( NNP/NNS/NN/NNPS ) ) ) ) )',
     '7.1.4' : '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NNP/NNS/NN/NNPS ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP:subject2-o ( NNP/NNS/NN/NNPS ) ( NNP/NNS/NN/NNPS ) ) ) ) )',
     '7.1.5' : '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP:subject2-o ( DT ) ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ) ) )',
     '7.1.6' : '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NNP/NNS/NN/NNPS ) ( NNP/NNS/NN/NNPS ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP:subject2-o ( NNP/NNS/NN/NNPS ) ( NNP/NNS/NN/NNPS ) ) ) ) )',
     '7.1.7' : '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NNP ) ( NNP ) ) ( NP ( DT ) ( NN:subject2-o ) ) )',
     '7.1.8' : '( SQ ( VBZ/VBD/VBP/VB/VBN ) ( NP:subject-o ( NN/NNS/NNP/NNPS ) ) ( VP ( VBZ/VBD/VBP/VB/VBN ) ( PP ( IN ) ( NP:subject2-o ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ) ) )',
     '7.1.9' : '( SQ ( VBZ/VBD/VBP/VBN/VB ) ( NP ( NN/NNS/NNP/NNPS:subject-o ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP ( NN/NNS/NNP/NNPS:subject2-o ) ) ) ) )',
     '7.1.10' : '( SQ ( VBZ/VBD/VBP/VBN/VB ) ( NP ( NN/NNS/NNP/NNPS:subject-o ) ) ( ADJP ( JJR:prop-o ) ( PP ( IN ) ( NP ( NN/NNS/NNP/NNPS:subject2-o ) ) ) ) )',
     '7.1.11' : '( SQ ( VBZ/VBD/VBP/VBN/VB ) ( NP ( EX ) ) ( NP ( NP:subject-o ( DT ) ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ( VP ( VBZ/VBD/VBP/VBN/VB ) ( NP:subject2-o ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ) ) )',
     
     #order
     '8.1.1' : '( SQ ( VP ( VB/VBZ/VBN/VBP/VBG ) ( NP ( PRP ) ) ( NP ( NP ( DT ) ( NN/NNS/NNP/NNPS:prop-o ) ) ( PP ( IN ) ( NP ( NN/NNS/NNP/NNPS:subject-o ) ) ) ) ) )',
     '8.1.2' : '( SQ ( VP ( VB/VBZ/VBN/VBP/VBG ) ( NP ( PRP ) ) ( NP ( PDT ) ( DT ) ( NN/NNS/NNP/NNPS:subject-o ) ) ) )',
     '8.1.3' : '( SQ ( VP ( VB/VBZ/VBN/VBP/VBG ) ( NP:subject-o ( DT ) ( JJ ) ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ) )',
     '8.1.4' : '( SQ ( VP ( VB/VBZ/VBN/VBP/VBG ) ( NP ( NP ( NN/NNS/NNP/NNPS ) ) ( VP ( VB/VBZ/VBN/VBP/VBG:prop-o ) ( PP ( IN ) ( NP:subject2-o ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ( NN/NNS/NNP/NNPS ) ) ) ) ) ) )'

}
        

def whichRulesMatched(matches, params, query) :
    
    idRules = ""
    dictCourant = dict_rules
    
    #on parcourt chaque match et on essaye de voir si on obtient une règle
    #chaque match correspond a une partie de la regle
    #donc a travers le dict_rules, on essaye de reconstituer la regle qui a
    #matchee
    
    for m in matches :
        
        if m in dictCourant.keys():
            if type(dictCourant[m]) == dict :
                dictCourant = dictCourant[m]
            else :
                idRules = dictCourant[m]
        #on reinitialise dictCourant à la racine du dictionnaire
        else :
            dictCourant = dict_rules
            idRules = ""
            
            
    if idRules :
        print("write suggestion")
        writeSuggestions(idRules, params, query)
        return all_rules[idRules] 
    return idRules

def writeSuggestions(idRules, params, query):
    
    filepath = "ihm/history/skeleton_query.csv"
    skeleton = ""
    query_lower = query.lower()
    row = []
    
    print("param",params)
    if params["qtype"] == "yesno" or params["qtype"] == "order" :
        if params["subject1"] :
            skeleton = query_lower.replace(params["subject1"],"(S1)")
        if params["subject2"] :
            skeleton = skeleton.replace(params["subject2"],"(S2)")
        if params["prop"] :
            skeleton = skeleton.replace(params["prop"],"(P)")

    else :
        
        if "subject" in params :
            skeleton = query_lower.replace(params["subject"],"(S)")
            
        elif "inst" in params :
            skeleton = query_lower.replace(params["inst"],"(S)")
            
        if "prop" in params :
            if params["prop"] :
                skeleton = skeleton.replace(params["prop"],"(P)")

        
    row = [idRules,params["qtype"],skeleton]
        
        
    if os.path.isfile(filepath) :
        #append mode = permet d'ajouter à un fichier existant
        with open(filepath, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
                
            writer.writerow(row)
                
        csvFile.close()
        
    else :
        with open(filepath, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
                
            writer.writerow(row)
                
        csvFile.close()
        
def readSuggestions():
    
    filepath = "ihm/history/skeleton_query.csv"
    skeletons = []
    #on charge le fichier lorsque l'appli s'ouvre
        
    #si le fichier de log existe alors on le lit et rempli le tableau
    if os.path.isfile(filepath) :
        #avant d'afficher on supprime
        #delimiter "," par defaut
        with open(filepath, 'r') as csvFile:
            reader = csv.reader(csvFile)
                
            for row in reader:
                if len(row) != 0 :
                    skeletons.append(row[2])

        csvFile.close()
    
    
    return set(skeletons)