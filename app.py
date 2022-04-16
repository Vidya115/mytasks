from configure.next_gen_lead_config import *
from models.product_enquiry_model import *
from models.dealer_model import *


@app.route('/getAllRecordsWithOutAnyCondition', methods=['GET'])
def getCustomRecords2112():
    log.info("getCustomRecords : Started")
    product_result = []
    dealer_code = request.args.get('dealer_code')
    log.debug("dealer_code is {}".format(dealer_code))

    try:
        product_result = session.query(ProductEnquiry).all()
        log.debug("product_result is {}".format(product_result))
    except Exception as err:
        session.rollback()
        log.error("error occured while product enquiry table sql transaction is {}". format(err))
    finally:
        session.close()
    product_result_dict = [item.__dict__ for item in product_result]
    log.debug("product_result_dict is {}".format(product_result_dict))
    for item in product_result_dict:
        del item['_sa_instance_state']
    log.info("getCustomRecords : Ended")
    return jsonify(product_result_dict)


@app.route('/getAllRecords', methods=['GET'])
def getCustomRecords():
    log.info("getCustomRecords : Started")
    currentdate = date.today()
    dealer_result = []
    product_result = []
    log.debug("current date is {}".format(currentdate))
    dealer_code = request.args.get('dealer_code')
    log.debug("dealer_code is {}".format(dealer_code))
    try:
        dealer_result = session.query(Dealer).filter(Dealer.dealerCode == dealer_code).all()
        log.debug("dealer_result is {}".format(dealer_result))
    except Exception as err:
        log.error("error occurred while product enquiry table sql transaction is {}", format(err))
        session.rollback()
    if dealer_result:
        try:
            product_result = session.query(ProductEnquiry).filter(ProductEnquiry.dealerCode == dealer_code).all()
            log.debug("product_result is {}".format(product_result))
        except Exception as err:
            session.rollback()
            log.error("error occured while product enquiry table sql transaction is {}". format(err))
        finally:
            session.close()
        product_result_dict = [item.__dict__ for item in product_result]
        log.debug("product_result_dict is {}".format(product_result_dict))
        for item in product_result_dict:
            del item['_sa_instance_state']
        log.info("getCustomRecords : Ended")
        return jsonify(product_result_dict)
    else:
        log.info("getCustomRecords : Ended")
        return "Unauthorized access"



@app.route('/del_single_record', methods=['DELETE'])
def del_record():
    log.info("delRecord : Started")
    mobile_number = request.args.get("mobile_number")
    log.debug("mobile_number is {}".format("mobile_number"))
    try:
        product_result = session.query(ProductEnquiry).filter(ProductEnquiry.mobileNumber == mobile_number).all()
        log.debug("product_result is {}".format(product_result))
        if product_result:
            pass
        else:
            return "Mobile number - {} records doesn't exist".format(mobile_number)
    except Exception as err:
        log.error("Error occurred is {}".format(err))
        session.rollback()
    try:
        product_result = session.query(ProductEnquiry).filter(ProductEnquiry.mobileNumber == mobile_number).delete()
        log.debug("product_result is {}".format(product_result))
        session.commit()
        return "Record has been deleted successfully"
    except Exception as err:
        log.error("Error occurred is {}".format(err))
        session.rollback()
    finally:
        session.close()


@app.route('/insert_records', methods=['POST'])
def insert_records():
    log.info("insert_records : Started")
    record = []

    request_body = request.get_json(force=True)
    log.debug("request_body is {}", format(request_body))

    for item in request_body:
        record = ProductEnquiry(customerName=item["customername"],
                                gender=item["gender"],
                                age=item["age"],
                                occupation=item["occupation"],
                                mobileNumber=item["mobileno"],
                                emailId=item["emailid"], )

        session.add_all([record])
    session.commit()

@app.route('/generic-fetch', methods=['GET'])
def genericFetch():

    log.info("genericFetch : Started")
    filter_condition = []
    product_result = []
    myDict = request.args
    log.debug("myDict is {}".format(myDict))

    if "mobile_num" in myDict:
        filter_condition.append(ProductEnquiry.mobileNumber == request.args.get("mobile_num"))
    if "email_id" in myDict:
        filter_condition.append(ProductEnquiry.emailId == request.args.get("email_id"))
    if "state" in myDict:
        filter_condition.append(ProductEnquiry.state == request.args.get("state"))
    if "vehicle_model" in myDict:
        filter_condition.append(ProductEnquiry.vehicleModel == request.args.get("vehicle_model"))
    if "district" in myDict:
        filter_condition.append(ProductEnquiry.district == request.args.get("district"))
    if "city" in myDict:
        filter_condition.append(ProductEnquiry.city == request.args.get("city"))
    if "age" in myDict:
            filter_condition.append(ProductEnquiry.age == request.args.get("age"))

    log.debug("Filter condition is {}".format(filter_condition))


    try:
        product_result = session.query(ProductEnquiry).filter(*filter_condition).all()
        log.debug("product_result is {}".format(product_result))
    except Exception as err:
        session.rollback()
        log.error("Error occured while ProductEnquiry table sql transaction is {}".format(err))
    finally:
        session.close()
    product_result_dict = [item.__dict__ for item in product_result]
    log.debug("product_result_dict is {}".format(product_result_dict))
    for item in product_result_dict:
        del item['_sa_instance_state']
    log.info("genericFetch : Ended")
    return jsonify(product_result_dict)




# Run the APP
app.run(debug=False)
