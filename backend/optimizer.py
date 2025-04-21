#!/usr/bin/env python3

import numpy as np

class StryktipsetOptimizer:
    def __init__(self, predictions, budget=100, risk_level='medium'):
        self.predictions = predictions
        self.budget = budget
        self.risk_level = risk_level
        
        # Översätt risknivå till numeriska parametrar
        self.risk_params = self._get_risk_parameters(risk_level)
    
    def _get_risk_parameters(self, risk_level):
        """Konfigurera parametrar baserat på risknivå"""
        if risk_level == 'low':
            return {
                'min_prob_for_single': 0.70,  # Min sannolikhet för spik
                'max_doubles': 4,            # Max antal halvgarderingar
                'max_triples': 1,            # Max antal helgarderingar
                'value_threshold': 1.2        # Värdegräns för garderingar
            }
        elif risk_level == 'medium':
            return {
                'min_prob_for_single': 0.60,
                'max_doubles': 6,
                'max_triples': 2,
                'value_threshold': 1.1
            }
        elif risk_level == 'high':
            return {
                'min_prob_for_single': 0.50,
                'max_doubles': 8,
                'max_triples': 3,
                'value_threshold': 1.05
            }
        else:
            raise ValueError(f"Ogiltig risknivå: {risk_level}")
    
    def optimize(self):
        """Optimera Stryktipset-system baserat på prediktioner, budget och risknivå"""
        # I en verklig implementation skulle man använda mer avancerad optimering
        # såsom heuristisk sökning, genetiska algoritmer eller något annat
        # För demos skull används en enkel regel-baserad strategi
        
        system = []
        
        for i, match in enumerate(self.predictions):
            probs = match['probabilities']
            home_prob = probs['1']
            draw_prob = probs['X']
            away_prob = probs['2']
            
            # Beräkna streck-simulering (stand-in för verklig streckfördelning)
            # I verkligheten skulle vi hämta detta från data
            total = home_prob + draw_prob + away_prob
            home_streck = home_prob / total
            draw_streck = draw_prob / total
            away_streck = away_prob / total
            
            # Beräkna värden (sannolikhet/streck)
            home_value = home_prob / home_streck if home_streck > 0 else 0
            draw_value = draw_prob / draw_streck if draw_streck > 0 else 0
            away_value = away_prob / away_streck if away_streck > 0 else 0
            
            # Sortera utfall efter sannolikhet
            outcomes = [
                {'outcome': '1', 'prob': home_prob, 'value': home_value},
                {'outcome': 'X', 'prob': draw_prob, 'value': draw_value},
                {'outcome': '2', 'prob': away_prob, 'value': away_value}
            ]
            outcomes.sort(key=lambda x: x['prob'], reverse=True)
            
            # Besluta om spik eller gardering baserat på risknivå
            selection = []
            
            # Om högsta sannolikhet är över tröskeln, spika
            if outcomes[0]['prob'] >= self.risk_params['min_prob_for_single']:
                selection.append(outcomes[0]['outcome'])
            # Annars, överväg halvgardering
            elif outcomes[0]['prob'] + outcomes[1]['prob'] >= 0.8:
                selection.extend([outcomes[0]['outcome'], outcomes[1]['outcome']])
            # Eller helgardering för mycket osäkra matcher
            else:
                selection.extend([o['outcome'] for o in outcomes])
            
            # Justera baserat på värde - lägg till utfall med högt värde
            for outcome in outcomes:
                if outcome['outcome'] not in selection and outcome['value'] >= self.risk_params['value_threshold']:
                    selection.append(outcome['outcome'])
            
            system.append({
                'match_index': i + 1,
                'home_team': match['home_team'],
                'away_team': match['away_team'],
                'selection': selection,
                'probabilities': match['probabilities']
            })
        
        # Justera systemet inom budgeten
        optimized_system = self._adjust_to_budget(system)
        
        # Beräkna några nyckeltal för systemet
        expected_value = self._calculate_expected_value(optimized_system)
        win_probability = self._calculate_win_probability(optimized_system)
        
        return {
            'system': optimized_system,
            'expected_value': expected_value,
            'win_probability': win_probability
        }
    
    def _adjust_to_budget(self, system):
        """Justera systemet för att passa inom budgeten"""
        # Beräkna nuvarande kostnad
        current_cost = self._calculate_system_cost(system)
        
        # Om systemet redan är inom budget, returnera det
        if current_cost <= self.budget:
            return system
        
        # Annars, reducera systemet genom att ta bort de minst värdefulla garderingarna
        adjusted_system = system.copy()
        
        # Samla alla halvgarderingar och helgarderingar
        candidates_for_reduction = []
        for i, match in enumerate(adjusted_system):
            if len(match['selection']) > 1:  # Gardering
                value_score = 0
                # Beräkna ett värdetal för hela garderingen
                for outcome in match['selection']:
                    value_score += match['probabilities'][outcome]
                
                candidates_for_reduction.append({
                    'match_index': i,
                    'value_score': value_score / len(match['selection']),
                    'current_selections': match['selection']
                })
        
        # Sortera kandidater efter värdescore (lägst först)
        candidates_for_reduction.sort(key=lambda x: x['value_score'])
        
        # Reducera tills vi är under budget
        for candidate in candidates_for_reduction:
            if current_cost <= self.budget:
                break
            
            match_idx = candidate['match_index']
            current_selections = candidate['current_selections']
            
            if len(current_selections) == 3:  # Helgardering -> halvgardering
                # Ta bort det minst sannolika utfallet
                probs = adjusted_system[match_idx]['probabilities']
                least_likely = min(current_selections, key=lambda x: probs[x])
                adjusted_system[match_idx]['selection'].remove(least_likely)
                
                # Uppdatera kostnad
                current_cost = self._calculate_system_cost(adjusted_system)
            elif len(current_selections) == 2:  # Halvgardering -> spik
                # Behåll bara det mest sannolika utfallet
                probs = adjusted_system[match_idx]['probabilities']
                most_likely = max(current_selections, key=lambda x: probs[x])
                adjusted_system[match_idx]['selection'] = [most_likely]
                
                # Uppdatera kostnad
                current_cost = self._calculate_system_cost(adjusted_system)
        
        return adjusted_system
    
    def _calculate_system_cost(self, system):
        """Beräkna kostnaden för systemet"""
        # För enkelhetens skull beräknas bara M-systemkostnad
        # I verkligheten skulle man kunna implementera reducerade system
        cost = 1
        for match in system:
            cost *= len(match['selection'])
        return cost
    
    def _calculate_expected_value(self, system):
        """Beräkna förväntat värde för systemet"""
        # För demo - returnera en simulering
        # I verkligheten skulle detta vara en mer komplex beräkning
        win_prob = self._calculate_win_probability(system)
        cost = self._calculate_system_cost(system)
        
        # Simulera förväntad utdelning baserat på systemstorlek och sannolikhet
        exp_return = cost * 2 * win_prob  # Förenkla: förvänta 2x återbetalning vid vinst
        exp_value = exp_return - cost
        
        return exp_value
    
    def _calculate_win_probability(self, system):
        """Beräkna sannolikheten att systemet ger vinst"""
        # För demo - simulera enkel beräkning
        # I verkligheten skulle detta vara mycket mer komplext
        
        # Beräkna sannolikheten att få 13 rätt för en specifik rad
        probs_product = 1.0
        
        for match in system:
            # Sannolikheten att få rätt på denna match är summan av 
            # sannolikheterna för de utfall som är med i systemet
            match_prob = sum(match['probabilities'][outcome] for outcome in match['selection'])
            probs_product *= match_prob
        
        return probs_product