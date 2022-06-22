# If a patient has more than one  subscription

@action(methods=["GET"], detail=False, url_path='retrieve-subscription')
def retrieve_patient_subscription_details(self, request):
     """
        Retrieve patients subscription details
            params:
                patient: patient_id,
                package_literal: mental-health
        """
        patient_id = request.query_params.get('patient')
        if patient_id:
            try:
                patient = Patient.objects.get(id=patient_id)
            except Patient.DoesNotExist:
                return Response({"detail": "Patient Not Found"}, status=status.HTTP_404_NOT_FOUND)
        package_literal = request.query_params.get('package_literal')
        package_name = URL_PARAMETER_MAP.get(package_literal)
        if package_name:
            try:
                subscription = Subscription.objects.filter(patient=patient,
                                                           plan__package_name=package_name).order_by('-created_at')
                serializer = ReadOnlySubscriptionSerializer(
                    subscription, many=True)
                breakpoint()
            except Subscription.DoesNotExist:
                return Response({"detail": " Subcription Not Found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
