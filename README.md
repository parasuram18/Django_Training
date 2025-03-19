# Django_Training


        # if method == "increase_by_amount":
            
        #     for objlist in [treatment,lab,consultant,room]:
            
        #         if apply_by == 'ip':
        #             field = ['in_patient']
        #             for obj in objlist:
        #                 obj.in_patient+=amount
    
        #         elif apply_by == 'op':
        #             field = ['out_patient']
        #             for obj in objlist:
        #                 obj.out_patient+=amount
                        
        #         elif apply_by == 'dc':
        #             field = ['daycare']
        #             for obj in objlist:
        #                 obj.daycare+=amount
                        
        #         elif apply_by == 'all':
        #             field = ['in_patient','out_patient','daycare']
        #             for obj in objlist:
        #                 obj.in_patient+=amount
        #                 obj.out_patient+=amount
        #                 obj.daycare+=amount
            
        #         # treatment_charges.objects.all().update(out_patient=F('out_patient')+amount)

        # elif method == "decrease_by_amount":
        #     for objlist in [treatment,lab,consultant,room]:
            
        #         if apply_by == 'ip':
        #             field = ['in_patient']
        #             for obj in objlist:
        #                 obj.in_patient-=amount
    
        #         elif apply_by == 'op':
        #             field = ['out_patient']
        #             for obj in objlist:
        #                 obj.out_patient-=amount
                        
        #         elif apply_by == 'dc':
        #             field = ['daycare']
        #             for obj in objlist:
        #                 obj.daycare-=amount
                        
        #         elif apply_by == 'all':
        #             field = ['in_patient','out_patient','daycare']
        #             for obj in objlist:
        #                 obj.in_patient-=amount
        #                 obj.out_patient-=amount
        #                 obj.daycare-=amount

        # elif method == "increase_by_percentage":
        #     per_val = percentage/100
        #     for objlist in [treatment,lab,consultant,room]:
            
        #         if apply_by == 'ip':
        #             field = ['in_patient']
        #             for obj in objlist:
        #                 obj.in_patient*=(1+per_val)
    
        #         elif apply_by == 'op':
        #             field = ['out_patient']
        #             for obj in objlist:
        #                 obj.out_patient*=(1+per_val)
                        
        #         elif apply_by == 'dc':
        #             field = ['daycare']
        #             for obj in objlist:
        #                 obj.daycare*=(1+per_val)
                        
        #         elif apply_by == 'all':
        #             field = ['in_patient','out_patient','daycare']
        #             for obj in objlist:
        #                 obj.in_patient*=(1+per_val)
        #                 obj.out_patient*=(1+per_val)
        #                 obj.daycare*=(1+per_val)

        # elif method == "decrease_by_percentage":
        #     per_val = percentage/100
        #     for objlist in [treatment,lab,consultant,room]:
            
        #         if apply_by == 'ip':
        #             field = ['in_patient']
        #             for obj in objlist:
        #                 obj.in_patient*=(1-per_val)
    
        #         elif apply_by == 'op':
        #             field = ['out_patient']
        #             for obj in objlist:
        #                 obj.out_patient*=(1-per_val)
                        
        #         elif apply_by == 'dc':
        #             field = ['daycare']
        #             for obj in objlist:
        #                 obj.daycare*=(1-per_val)
                        
        #         elif apply_by == 'all':
        #             field = ['in_patient','out_patient','daycare']
        #             for obj in objlist:
        #                 obj.in_patient*=(1-per_val)
        #                 obj.out_patient*=(1-per_val)
        #                 obj.daycare*=(1-per_val)
                
        # treatment_charges.objects.bulk_update(treatment,field)
        # lab_charges.objects.bulk_update(lab,field)
        # consultant_charges.objects.bulk_update(consultant,field)
        # room_master.objects.bulk_update(room,field)