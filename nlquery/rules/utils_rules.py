# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:53:31 2019

@author: Dorian
"""
from nltk.tree import Tree
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame
import os

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
	'( SQ ( VBZ/VBD/VBP ) ( NP:subject-o ( NNP/NNS/NN ) ( NNP/NNS/NN ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP:subject2-o ( NNP/NNS/NN ) ( NNP/NNS/NN ) ) ) ) )' : '7.1.1',
    '( SQ ( VBZ/VBD/VBP:action-o ) ( NP:subject-o ( NNP ) ( NNP ) ) ( ADJP ( JJ:prop-o ) ) )' : '7.1.2',
    '( SQ ( VBZ/VBD/VBP:action-o ) ( NP:subject-o ( NNP ) ( NNP ) ) ( NP ( DT ) ( NN:subject2-o ) ) )' : '7.1.3',
    '( SQ ( VBZ/VBD/VBP ) ( NP ( NNP:subject-o ) ) ( VP ( VBN:prop-o ) ( PP ( IN ) ( NP:subject2-o ( NNP ) ( NNPS ) ) ) ) )' : '7.1.4',
    '( SQ ( VBZ/VBD/VBP ) ( NP ( NNP:subject-o ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP ( NNP:subject2-o ) ) ) ) )' : '7.1.5',
    '( SQ ( VBZ/VBD/VBP ) ( NP ( NNP:subject-o ) ) ( ADJP ( JJR:prop-o ) ( PP ( IN ) ( NP ( NNP:subject2-o ) ) ) ) )' : '7.1.6'
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
     '7.1.1' : '( SQ ( VBZ/VBD/VBP ) ( NP:subject-o ( NNP/NNS/NN ) ( NNP/NNS/NN ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP:subject2-o ( NNP/NNS/NN ) ( NNP/NNS/NN ) ) ) ) )',
     '7.1.2' : '( SQ ( VBZ/VBD/VBP:action-o ) ( NP:subject-o ( NNP ) ( NNP ) ) ( ADJP ( JJ:prop-o ) ) )',
     '7.1.3' : '( SQ ( VBZ/VBD/VBP:action-o ) ( NP:subject-o ( NNP ) ( NNP ) ) ( NP ( DT ) ( NN:subject2-o ) ) )',
     '7.1.4' : '( SQ ( VBZ/VBD/VBP ) ( NP ( NNP:subject-o ) ) ( VP ( VBN:prop-o ) ( PP ( IN ) ( NP:subject2-o ( NNP ) ( NNPS ) ) ) ) )',
     '7.1.5' : '( SQ ( VBZ/VBD/VBP ) ( NP ( NNP:subject-o ) ) ( NP ( NP ( JJR:prop-o ) ) ( PP ( IN ) ( NP ( NNP:subject2-o ) ) ) ) )',
     '7.1.6' : '( SQ ( VBZ/VBD/VBP ) ( NP ( NNP:subject-o ) ) ( ADJP ( JJR:prop-o ) ( PP ( IN ) ( NP ( NNP:subject2-o ) ) ) ) )'
}
        

def whichRulesMatched(matches) :
    
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
        return all_rules[idRules] 
    return idRules


            
def createImageOfRules(rules) :
    
    for k,v in rules.items() :
        numberRule = k.replace(".","_")
        filenamePS = "ihm/rules_image/rule-%s.ps"%numberRule
        filenamePNG = "ihm/rules_image/rule-%s.png"%numberRule
    
        cf = CanvasFrame()
            
        tr = Tree.fromstring(v)
        tc = TreeWidget(cf.canvas(),tr)
            
        tc['node_font'] = 'arial 13 bold'
        tc['leaf_font'] = 'arial 11'
        tc['node_color'] = '#005990'
        tc['leaf_color'] = '#3F8F57'
        tc['line_color'] = '#175252'
        tc['xspace'] = 25
        tc['yspace'] = 25
            
        cf.add_widget(tc,10,10) # (10,10) offsets
            
        cf.print_to_file(filenamePS)
        cf.destroy()
            
        #MagickImage doit etre installée ainsi que convert
        os.system("convert %s %s" % (filenamePS, filenamePNG))
        
if __name__ == "__main__":
    createImageOfRules(all_rules)     