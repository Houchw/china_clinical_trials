# -*- coding: utf-8 -*-
import scrapy
from china_clinical_trials.items import ChinaClinicalTrialsItem

class ClinicalSpiderSpider(scrapy.Spider):
    name = 'clinical_spider'
    allowed_domains = ['chinadrugtrials.org.cn']
    start_urls = ["http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlistdetail?ckm_index={}&currentpage=1&pagesize=20&rule=CTR&sort=desc&sort2=desc".format(i) for i in range(1, 6864)]
    
    
    def parse(self, response):
        tables = response.xpath('//*[@id="div_open_close_01"]/table')
        
        item = ChinaClinicalTrialsItem()
        
        # 首次公示信息日期
    
        # item['first_public_date'] = response.xpath("/html/body/div/table/tbody/tr[2]/td/div[2]/div/div[2]/div[1]/div[3]/table/tbody/tr[2]/td[4]/text()").extract()[0].strip()
        
        # 题目和背景信息
        trs = tables[0].xpath('tr')
        
        item['ctr_number'] = trs[0].xpath('td[2]/text()').extract()[0].strip() #登记号
        item['conditions'] = trs[1].xpath('td[2]/text()').extract()[0].strip() #适应症
        item['public_title'] = trs[2].xpath('td[2]/text()').extract()[0].strip() #试验通俗题目
        item['scientific_title'] = trs[3].xpath('td[2]/text()').extract()[0].strip()  #试验专业题目
        item['plan_version'] = trs[4].xpath('td[2]/text()').extract()[0].strip() #试验方案编号
        item['accept_id'] = trs[5].xpath('td[2]/text()').extract()[0].strip() #临床申请受理号
        item['drug_name'] = trs[6].xpath('td[2]/text()').extract()[0].strip() #药物名称
        item['drug_type'] = trs[7].xpath('td[2]/text()').extract()[0].strip() #化学药物
        #print("题目和背景信息")
        #print(item)
        
        # 申办者信息
        trs = tables[1].xpath('tr')
        if len(trs[0].xpath('td[2]/table')) == 0:
            item['sponsors'] = trs[0].xpath('td[2]/text()').extract()[0].strip() #申办者名称
        else:
            # 处理申办者信息在表格中的情况
            item['sponsors'] = ''.join([s.strip() for s in trs[0].xpath('td/table/tr/td[2]/text()').extract()])
        
        item['applicant'] = trs[1].xpath('td[2]/text()').extract()[0].strip() #联系人姓名
        item['applicant_telephone'] = trs[2].xpath('td[2]/text()').extract()[0].strip() #联系人电话
        item['applicant_Email'] = trs[2].xpath('td[4]/text()').extract()[0].strip() #联系人邮箱
        item['applicant_address'] = trs[3].xpath('td[2]/text()').extract()[0].strip() #联系人邮政地址
        item['applicant_postcode'] = trs[3].xpath('td[4]/text()').extract()[0].strip() #联系人邮编
        item['sources_of_funding'] = trs[4].xpath('td[2]/text()').extract()[0].strip() #试验项目经费来源
        #print("申办者信息")
        #print(item)
        # 临床试验信息
        trs = tables[2].xpath('tr')
        
        item['purpose'] = trs[1].xpath('td/text()').extract()[0].strip() # 试验目的
        
        ## 试验设计
        tmp_trs = trs[3].xpath('td/table/tr/td[3]/text()').extract()
        tmp_trs = [s.strip() for s in tmp_trs]
        
        item['study_type'] = tmp_trs[0] # 试验分类
        item['phase'] = tmp_trs[1] # 试验分期
        item['intervention_model'] = tmp_trs[2] #设计类型
        item['allocation'] = tmp_trs[3] #随机化
        item['masking'] = tmp_trs[4] #盲法
        item['study_domain'] = tmp_trs[5] #试验范围
        
        ## 受试者信息
        
        item['age'] = ''.join(trs[5].xpath('td[2]/text()').extract()[0].strip().split()) #年龄
        item['gender'] = trs[6].xpath('td[2]/text()').extract()[0].strip() #性别
        item['accepts_healthy_volunteers'] = trs[7].xpath('td[2]/text()').extract()[0].strip() #健康受试者：有或无
        
        tmp_trs = trs[8].xpath('td/table/tr')
        tmp_trs = [s.strip() for s in tmp_trs.xpath('td[2]/text()').extract()]
        item['inclusion_criteria'] = '|'.join(tmp_trs) #入选标准
        
        tmp_trs = trs[9].xpath('td/table/tr')
        tmp_trs = [s.strip() for s in tmp_trs.xpath('td[2]/text()').extract()]
        item['exclusion_criteria'] = '|'.join(tmp_trs) #排除标准
        
        tmp_trs = trs[10].xpath('td[2]/text()').extract()
        item['estimated_enrollment'] = ''.join(s.strip() for s in tmp_trs) #目标入组人数
        
        tmp_trs = trs[11].xpath('td[2]/text()').extract()
        item['actual_enrollment'] = ''.join(s.strip() for s in tmp_trs) #实际入组人数
        
        
        ## 试验分组
        tmp_trs = trs[13].xpath('td/table/tr/td[2]/text()').extract()[1:]
        item['experimental_drug_name'] = '|'.join([s.strip() for s in tmp_trs]) #试验药名称
        
        tmp_trs = trs[13].xpath('td/table/tr/td[3]/text()').extract()[1:]
        item['experimental_drug_usage'] = '|'.join([s.strip() for s in tmp_trs]) #试验药用法
        
        tmp_trs = trs[14].xpath('td/table/tr/td[2]/text()').extract()[1:]
        item['placebo_drug_name'] = '|'.join([s.strip() for s in tmp_trs]) #对照药名称
        
        tmp_trs = trs[14].xpath('td/table/tr/td[3]/text()').extract()[1:]
        item['placebo_drug_usage'] = '|'.join([s.strip() for s in tmp_trs]) #对照药用法
        
        
        ## 终点指标
        tmp_trs = trs[16].xpath('td/table/tr/td[2]/text()').extract()[1:]
        item['primary_outcome_measures'] = '|'.join([s.strip() for s in tmp_trs]) #主要终点指标
        
        tmp_trs = trs[16].xpath('td/table/tr/td[3]/text()').extract()[1:]
        item['primary_outcome_measures_date'] = '|'.join([s.strip() for s in tmp_trs]) #评价时间
        
        tmp_trs = trs[16].xpath('td/table/tr/td[4]/text()').extract()[1:]
        item['primary_outcome_measures_choice'] = '|'.join([s.strip() for s in tmp_trs]) #终点指标选择
        
        tmp_trs = trs[17].xpath('td/table/tr/td[2]/text()').extract()[1:]
        item['secondary_outcome_measures'] = '|'.join([s.strip() for s in tmp_trs]) #次要终点指标
        
        tmp_trs = trs[17].xpath('td/table/tr/td[3]/text()').extract()[1:]
        item['secondary_outcome_measures_date'] = '|'.join([s.strip() for s in tmp_trs]) #评价时间
        
        tmp_trs = trs[17].xpath('td/table/tr/td[4]/text()').extract()[1:]
        item['secondary_outcome_measures_choice'] = '|'.join([s.strip() for s in tmp_trs]) #终点指标选择
        
        
        ## 数据安全监察委员会
        item['data_management_committee'] = trs[18].xpath('td/text()').extract()[0].strip()[-1]
        
        ## 为受试者购买试验伤害保险
        item['insurance_for_subject'] = trs[19].xpath('td/text()').extract()[0].strip()[-1]
        
        # 第一例受试者入组日期
        item['first_subject_included_date'] = tables[3].xpath('tr/td/text()').extract()[0].strip()
        
        # 试验终止日期
        item['study_ending_date'] = tables[4].xpath('tr/td/text()').extract()[0].strip()
        
        
        # 研究者信息
        tmp_tables = tables[5].xpath('tr/td/table')
        
        ## 主要研究者信息
        
        item['study_leader_name'] = tmp_tables[0].xpath('td[2]/text()').extract()[0].strip()
        item['study_leader_title'] = tmp_tables[0].xpath('td[4]/text()').extract()[0].strip() #职称
        
        tmp_tds_2 = [s.strip() for s in tmp_tables[0].xpath('tr/td[2]/text()').extract()]
        tmp_tds_4 = [s.strip() for s in tmp_tables[0].xpath('tr/td[4]/text()').extract()]
        item['study_leader_phone'] = tmp_tds_2[0]
        item['study_leader_email'] = tmp_tds_4[0]
        item['study_leader_address'] = tmp_tds_2[1]
        item['study_leader_postcode'] = tmp_tds_4[1]
        item['study_leader_institution'] = tmp_tds_2[2]
        
        
        ## 各参加机构信息
        
        tmp_tds = [s.strip() for s in tmp_tables[1].xpath('tr/td[2]/text()').extract()[1:]]
        item['study_site_name'] = '|'.join(tmp_tds)
        
        tmp_tds = [s.strip() for s in tmp_tables[1].xpath('tr/td[3]/text()').extract()[1:]]
        item['study_site_pi'] = '|'.join(tmp_tds)
        
        tmp_tds = [s.strip() for s in tmp_tables[1].xpath('tr/td[4]/text()').extract()[1:]]
        item['study_site_country'] = '|'.join(tmp_tds)
        
        tmp_tds = [s.strip() for s in tmp_tables[1].xpath('tr/td[5]/text()').extract()[1:]]
        item['study_site_province'] = '|'.join(tmp_tds)
        
        tmp_tds = [s.strip() for s in tmp_tables[1].xpath('tr/td[6]/text()').extract()[1:]]
        item['study_site_city'] = '|'.join(tmp_tds)
        
        
        # 伦理委员会信息
        
        tmp_tds = [s.strip() for s in tables[6].xpath('tr/td[2]/text()').extract()[1:]]
        item['ethic_committee_name'] = '|'.join(tmp_tds)
        
        tmp_tds = [s.strip() for s in tables[6].xpath('tr/td[3]/text()').extract()[1:]]
        item['ethic_committee_approved'] = '|'.join(tmp_tds)
        
        tmp_tds = [s.strip() for s in tables[6].xpath('tr/td[4]/text()').extract()[1:]]
        item['ethic_committee_approved_date'] = '|'.join(tmp_tds)
        
        
        # 试验状态
        tmp_tds = [s.strip() for s in tables[7].xpath('tr/td/text()').extract()[0].strip().split()]
        item['recruitment_status'] = '|'.join(tmp_tds)
        
        #print("试验状态")
        #print(item)
        """
        # 信息更新记录
        updated_date = scrapy.Field() #信息更新时间
        updated_recored = scrapy.Field() # 信息更新记录
        """
        n = response.url.split('ckm_index=')[1].split('&')[0]
        n = int(n)
        print("当前进度为：{:.2f}%".format(n/6863.0*100))
        return(item)
