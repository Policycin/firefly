from urllib.parse import urlencode, quote, unquote
class Pagination(object):
    """
    自定义分页
    """
    def __init__(self, current_page, total_count, base_url, params, per_page_count=10, max_pager_count=11):
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1
        if current_page <= 0:
            current_page = 1
        self.current_page = current_page
        # 数据总条数
        self.total_count = total_count

        # 每页显示10条数据
        self.per_page_count = per_page_count

        # 页面上应该显示的最大页码
        max_page_num, div = divmod(total_count, per_page_count)
        if div:
            max_page_num += 1
        self.max_page_num = max_page_num

        # 页面上默认显示11个页码（当前页在中间）
        self.max_pager_count = max_pager_count
        self.half_max_pager_count = int((max_pager_count - 1) / 2)

        # URL前缀
        self.base_url = base_url

        # request.GET
        import copy
        params = copy.deepcopy(params)
        # params._mutable = True
        get_dict = params.to_dict()
        # 包含当前列表页面所有的搜/索条件
        # {source:[2,], status:[2], gender:[2],consultant:[1],page:[1]}
        # self.params[page] = 8
        # self.params.urlencode()
        # source=2&status=2&gender=2&consultant=1&page=8
        # href="/hosts/?source=2&status=2&gender=2&consultant=1&page=8"
        # href="%s?%s" %(self.base_url,self.params.urlencode())
        self.params = get_dict

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

    def page_html(self):
        # 如果总页数 <= 11
        if self.max_page_num <= self.max_pager_count:
            pager_start = 1
            pager_end = self.max_page_num
        # 如果总页数 > 11
        else:
            # 如果当前页 <= 5
            if self.current_page <= self.half_max_pager_count:
                pager_start = 1
                pager_end = self.max_pager_count
            else:
                # 当前页 + 5 > 总页码
                if (self.current_page + self.half_max_pager_count) > self.max_page_num:
                    pager_end = self.max_page_num
                    pager_start = self.max_page_num - self.max_pager_count + 1  # 倒这数11个
                else:
                    pager_start = self.current_page - self.half_max_pager_count
                    pager_end = self.current_page + self.half_max_pager_count

        page_html_list = []
        # {source:[2,], status:[2], gender:[2],consultant:[1],page:[1]}
        # 首页
        self.params['page'] = 1
        first_page = '<li><a href="%s?%s">首页</a></li>' % (self.base_url, urlencode(self.params),)
        page_html_list.append(first_page)
        # 上一页
        self.params["page"] = self.current_page - 1
        if self.params["page"] < 1:
            pervious_page = '<li class="disabled"><a href="%s?%s" aria-label="Previous">上一页</span></a></li>' % (
            self.base_url, urlencode(self.params))
        else:
            pervious_page = '<li><a href = "%s?%s" aria-label = "Previous" >上一页</span></a></li>' % (
            self.base_url, urlencode(self.params))
        page_html_list.append(pervious_page)
        # 中间页码
        for i in range(pager_start, pager_end + 1):
            self.params['page'] = i
            if i == self.current_page:
                temp = '<li class="active"><a href="%s?%s">%s</a></li>' % (self.base_url, urlencode(self.params), i,)
            else:
                temp = '<li><a href="%s?%s">%s</a></li>' % (self.base_url, urlencode(self.params), i,)
            page_html_list.append(temp)

        # 下一页
        self.params["page"] = self.current_page + 1
        if self.params["page"] > self.max_page_num:
            self.params["page"] = self.current_page
            next_page = '<li class="disabled"><a href = "%s?%s" aria-label = "Next">下一页</span></a></li >' % (
            self.base_url, urlencode(self.params))
        else:
            next_page = '<li><a href = "%s?%s" aria-label = "Next">下一页</span></a></li>' % (
            self.base_url, urlencode(self.params))
        page_html_list.append(next_page)

        # 尾页
        self.params['page'] = self.max_page_num
        last_page = '<li><a href="%s?%s">尾页</a></li>' % (self.base_url, urlencode(self.params),)
        page_html_list.append(last_page)

        return ''.join(page_html_list)

'''
totalFileCount = 0
            totalRowCount = 0
            fileNo2 = request.values.get("fileNo2")
            app.logger.info("fileNo2=%s" % fileNo2)
            sqlwhereOne = {}
            curDbName.statements.remove(sqlwhereOne)
            sqlwhereOne = {'fileNo': fileNo2}
            entities2 = curDbName.statements_all.find(sqlwhereOne)
            entities2Count = entities2.count()
            for x in range(entities2Count):
                entitiesMap = entities2[x]
                curDbName.statements.insert_one(entitiesMap)
#----------------------------------------------------------
            if entities2Count > 1:
                patternQiantou = re.compile(r'(（).*?牵头.*?(）)')
                patternFuze = re.compile(r'(（).*?负责.*?(）)')

                weightData = {}
                sqlwhereWeight = {'weight': {'$exists': 1}}
                entitiesWeight = curDbName.statements.find(sqlwhereWeight)
                for doc in entitiesWeight:
                    keyText = doc['text']
                    keyText = keyText.replace('20180308', '')
                    weightData[keyText] = doc['weight']
                # app.logger.info(weightData)

                sqlwhere = {}
                if len(repositoryID) > 2:
                    sqlwhere = {'_id': ObjectId(repositoryID)}
                else:
                    fileName = request.values.get("fileName")
                    fileNo = request.values.get("fileNo")
                    publisherCityName = request.values.get("publisherCityName")
                    if fileName is not None and len(fileName.strip()) > 0:
                        sqlfileName = {'fileName': re.compile(fileName)}
                        sqlwhere.update(sqlfileName)
                    if fileNo is not None and len(fileNo.strip()) > 0:
                        sqlfileNo = {'fileNo': re.compile(fileNo)}
                        sqlwhere.update(sqlfileNo)
                    if publisherCityName is not None and len(publisherCityName.strip()) > 0:
                        sqlTmp = {'publisherCityName': re.compile(publisherCityName)}
                        sqlwhere.update(sqlTmp)

                    publishtime1 = request.values.get("publishtime1")
                    publishtime2 = request.values.get("publishtime2")
                    if publishtime1 is not None and len(publishtime1.strip()) > 0:
                        sqlanswer = {'publishDate': {'$gte': publishtime1}}
                        sqlwhere.update(sqlanswer)
                    else:
                        publishtime1 = ""
                    if publishtime2 is not None and len(publishtime2.strip()) > 0:
                        if len(publishtime1) > 0:
                            sqlanswer = {'publishDate': {'$gte': publishtime1, '$lt': publishtime2}}
                        else:
                            sqlanswer = {'publishDate': {'$lt': publishtime2}}
                        sqlwhere.update(sqlanswer)

                app.logger.info(sqlwhere)
                entities = curDbName.CapFileCollection.find(sqlwhere)
                # app.logger.info("entities.count()=%d,entities2.count()=%d" % (entities.count(),entities2.count()))

                strFileNo2 = entities2[0]['fileNo']
                threshold = 45
                if 'threshold' in entities2[0]:
                    threshold = entities2[0]['threshold']
                threshold = float(threshold)
                bot.logic.get_adapters()[1].confidence_threshold = threshold / 100.0
                # app.logger.info("相似阈值：%.1f" % threshold)

                allCreate1 = datetime.today()
                timeConsuming5 = allCreate1 - allCreate1
                timeConsuming6 = timeConsuming5

                totalCount = entities.count()  # 总记录数
                # if totalCount > 4 :
                #    totalCount = 4
                for x in range(totalCount):
                    create_at1 = datetime.today()
                    huidaConfidenceSum = 0.0  # 相似字数乘以相似值
                    questionLengthSum = 0.0  # 文件总字符数
                    questionRowSum = 0  # 文件总行数
                    huidaLengthSum = 0.0  # 匹配总字符数
                    huidaRowSum = 0  # 匹配总行数
                    entitiesMap = entities[x]
                    serverFilename = entitiesMap['fileLocalUrl']
                    # app.logger.info("serverFilename%s" % serverFilename)
                    sqlwhere = {"fileID": entitiesMap['_id'], "fileNo2": strFileNo2}
                    curDbName.ConfidenceDetail.remove(sqlwhere)
                    sqlwhere = {"fileNo": entitiesMap['fileNo'], "fileNo2": strFileNo2}
                    curDbName.ConfidenceResult.remove(sqlwhere)
                    # update({"username":"111"},{"$pull":{"relationships":{"friends":"22"}}})
                    sqlwhere = {'_id': ObjectId(entitiesMap['_id'])}
                    sqlRTN = curDbName.CapFileCollection.update(sqlwhere,
                                                                {"$pull": {"fileConfidence": {"fileNo2": strFileNo2}}})
                    # app.logger.info(sqlRTN)
                    #------------------------------------------------------------
                    isInclude = 0  # 文件中是否包含对比字号 strFileNo2
                    try:
                        create_at61 = datetime.today()
                        with open(serverFilename, mode='r', encoding='utf-8') as txtFile:
                            allLines = txtFile.readlines()
                            create_at62 = datetime.today()
                            timeConsuming6 += (create_at62 - create_at61)
                            isBreak = 0
                            iFileConfidenceRowCount = 0
                            i = 0
                            for line in allLines:
                                line = line.strip()
                                line = line.replace(" ", "")
                                if line.find(strFileNo2) >= 0:
                                    app.logger.info("包含对比文件字号：%s" % strFileNo2)
                                    isInclude = 1
                                if (len(line) <= 4):
                                    continue
                                # app.logger.info(line)
                                strSub = re.split('。|；', line)
                                for question in strSub:
                                    i += 1
                                    question = question.strip()
                                    # if (len(question) <= 2):
                                    #    continue
                                    if (len(question.encode()) <= 17):
                                        # app.logger.info("question=%s,length=%d,length2=%d"%(question,len(question.encode()),len(question)))
                                        continue
                                    if question == "（此件公开发布）":
                                        isBreak = 1
                                        break
                                    # 除掉 牵头
                                    if patternQiantou.search(question) is not None:
                                        app.logger.info("除掉 牵头：question=%s" % question)
                                        continue
                                    if patternFuze.search(question) is not None:
                                        app.logger.info("除掉 负责：question=%s" % question)
                                        continue
                                    if i > 25 and iFileConfidenceRowCount == 0:  # 如果前25句中还没有一个相似就退出
                                        isBreak = 1
                                        break
                                    create_at51 = datetime.today()
                                    statementRes = bot.get_response(question)
                                    create_at52 = datetime.today()
                                    timeConsuming5 += (create_at52 - create_at51)
                                    huida = statementRes.text
                                    if patternQiantou.search(huida) is not None:
                                        app.logger.info("除掉 牵头：huida=%s" % huida)
                                        continue
                                    if patternFuze.search(huida) is not None:
                                        app.logger.info("除掉 负责：huida=%s" % huida)
                                        continue

                                    if strFileNo2 in huida:
                                        app.logger.info("相同字号：strFileNo2=%s,huida=%s" % (strFileNo2, huida))
                                        continue
                                    questionLengthSum += len(question)
                                    questionRowSum += 1
                                    huidaConfidence = 0

                                    if '对不起这个问题正在学习中20180308' == huida:
                                        huida = huida.replace("对不起这个问题正在学习中20180308", "")
                                    else:
                                        if i < 25:
                                            iFileConfidenceRowCount += 1

                                        huidaConfidence = statementRes.confidence
                                        huida = huida.replace("20180308", "")

                                        if huida in weightData:
                                            huidaConfidence = huidaConfidence * weightData[huida]
                                            if huidaConfidence > 1:
                                                huidaConfidence = 1
                                            # app.logger.info("huidaConfidence=%f,weightData[huida]=%f" , huidaConfidence, weightData[huida])

                                        huidaConfidenceSum += huidaConfidence * len(question)
                                        huidaLengthSum += len(question)
                                        huidaRowSum += 1

                                    sqlInsert = {"fileID": entitiesMap['_id'], "fileNo": entitiesMap['fileNo'],
                                                 "fileNo2": strFileNo2, "sentence": question,
                                                 "sentenceConfidence": huida,
                                                 "huidaConfidence": huidaConfidence * 100.0}
                                    curDbName.ConfidenceDetail.insert_one(sqlInsert)
                                if isBreak == 1:
                                    break
                                # app.logger.info("question=%s,huida=%s,huidaConfidence=%.2f" % (question,huida,huidaConfidence))


                    except Exception:
                        app.logger.info("产生例外的fileLocalUrl=%s" % serverFilename)
                        continue

                    if questionRowSum == 0 or questionLengthSum == 0:
                        continue

                    create_at2 = datetime.today()
                    timeConsuming = create_at2 - create_at1
                    # app.logger.info('耗时=%s,相似字数乘以相似值=%.2f,相似字数=%.2f,总字数=%.2f,相似语句数=%d,总语句数=%d,'
                    #                '总加权相似比=%.2f,相似字占比=%.2f,相似语句占比=%.2f'%(timeConsuming,huidaConfidenceSum,huidaLengthSum,questionLengthSum,huidaRowSum,questionRowSum,
                    #                huidaConfidenceSum/questionLengthSum*100.0,huidaLengthSum/questionLengthSum*100.0,huidaRowSum/questionRowSum*100.0))

                    sqlInsert = {"huidaConfidenceSum": huidaConfidenceSum, "huidaLengthSum": huidaLengthSum,
                                 "questionLengthSum": questionLengthSum,
                                 "huidaRowSum": huidaRowSum, "questionRowSum": questionRowSum,
                                 "statementConfidence": huidaConfidenceSum / questionLengthSum * 100.0,
                                 "fileNo": entitiesMap['fileNo'], "fileNo2": strFileNo2, "isInclude": isInclude,
                                 "timeConsuming": timeConsuming.seconds,
                                 "createTime": strCreate_at}

                        curDbName.ConfidenceResult.insert_one(sqlInsert)

                    confidenceJson = {"fileNo2": strFileNo2,
                                      "statementConfidence": huidaConfidenceSum / questionLengthSum * 100.0,
                                      "isInclude": isInclude}
                    sqlset2 = {'$push': {"fileConfidence": confidenceJson}}
                    # sqlset = {'$set': confidenceJson}
                    sqlwhere = {'_id': ObjectId(entitiesMap['_id'])}

                    # curDbName.CapFileCollection.update(sqlwhere, sqlset)
                    curDbName.CapFileCollection.update(sqlwhere, sqlset2)

                    totalFileCount = totalFileCount + 1
                    totalRowCount = totalRowCount + questionRowSum
                    # app.logger.info('处理文件数=%d'%(totalFileCount))
                allCreate2 = datetime.today()
                app.logger.info('总耗时=%s,文件总数=%d,总行数=%d,总耗时5=%s,总耗时6=%s' % (
                allCreate2 - allCreate1, totalFileCount, totalRowCount, timeConsuming5, timeConsuming6))

'''